from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import BaseManager
from core.exceptions import MaxLengthValidationError
from core.middleware import AccessLogMiddleware


class AbstractValidatableModel(models.Model):
    """Base model to inherit for all other models in gulfstream project.

    It implements validation logic and ensures that clean method and max
    length validation called before model save.
    """

    objects = BaseManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Save entity to database."""

        self.clean()
        self.validate_max_length()
        return super().save(*args, **kwargs)

    def validate_max_length(self):
        """Validate all model fields which has max_length attribute."""

        failed_fields = []

        for model_field in self._meta.get_fields():
            if isinstance(model_field, models.CharField):
                field_value = model_field.value_to_string(self)
                if not field_value:
                    continue

                field_value_length = len(field_value)
                if field_value_length > model_field.max_length:
                    failed_fields.append(
                        (
                            model_field.verbose_name,
                            model_field.name,
                            field_value_length,
                            model_field.max_length,
                        )
                    )

        if failed_fields:
            error_dict = {}
            for (
                verbose_name,
                field_name,
                value_length,
                max_length,
            ) in failed_fields:
                error_dict[field_name] = [
                    f'{verbose_name}: Value is too long({max_length}->{value_length})'
                ]
            raise MaxLengthValidationError(error_dict)


class AbstractCreatedUpdatedModel(AbstractValidatableModel):
    created = models.DateTimeField(('Created'), auto_now_add=True)
    updated = models.DateTimeField(('Updated'), auto_now=True)

    class Meta:
        abstract = True


class AbstractCreatedByUpdatedByModel(AbstractCreatedUpdatedModel):
    """Abstract class for models, which tracks user who created/updated it."""

    created_by = models.ForeignKey(
        'userauths.User',
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        verbose_name=_('Created by'),
    )
    updated_by = models.ForeignKey(
        'userauths.User',
        models.SET_NULL,
        related_name='+',
        verbose_name=_('Updated by'),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """Save entity to the database, updating created_by and updated_by."""
        update_fields = set(kwargs.get('update_fields') or [])
        user_id = self._get_user_id()
        if self.id is None and not self.created_by:
            self.created_by_id = user_id
            if update_fields:
                update_fields.add('created_by_id')
        elif self.id is not None:
            self.updated_by_id = user_id
            if update_fields:
                # Always update updated_by_id and updated
                update_fields |= {'updated_by_id', 'updated'}

        if update_fields:
            kwargs['update_fields'] = list(update_fields)

        super().save(*args, **kwargs)

    def _get_user_id(self):
        return AccessLogMiddleware.get_current_user_id()
