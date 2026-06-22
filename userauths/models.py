from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import uuid
from functools import cached_property

from core.db import AbstractCreatedByUpdatedByModel
from core.managers import UsersManager


class User(AbstractUser, AbstractCreatedByUpdatedByModel):
    """User entity."""

    username = None  # type: ignore
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    email = models.EmailField(_('Email address'), unique=True)
    last_activity = models.DateField(_('Last activity'), blank=True, null=True)
    event_tracking_id = models.UUIDField(
        _('Event Tracking ID'), default=uuid.uuid4, unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UsersManager()

    logging_tag = 'users'

    class Meta:
        """User meta info."""

        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'gulfstream-users_user'

    def save(self, *args, **kwargs):
        """Save entity to database."""
        if self.email:
            self.email = self.email.lower()
        return super().save(*args, **kwargs)

    def activate(self):
        """Activate user."""
        self.is_active = True
        self.save()

    def deactivate(self):
        """Deactivate user."""
        self.is_active = False
        self.save()

    @cached_property
    def date_format(self) -> str:
        """Return user date format from preferences."""
        return self.preferences.date_format.value

    @cached_property
    def time_format(self) -> str:
        """Return user time format from preferences."""
        return self.preferences.time_format.value

    @cached_property
    def timezone(self) -> str:
        """Return user timezone str from preferences."""
        return self.preferences.timezone.value
