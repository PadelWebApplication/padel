from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_enum.fields import EnumCharField

from userauths import models as userauth_model
from services.coach.enum import NotificationTypeChoices


class Coach(models.Model):
    user = models.OneToOneField(userauth_model.User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images', null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.CharField(max_length=100, null=True, blank=True)
    next_available_session_date = models.CharField(
        max_length=100, null=True, blank=True
    )

    def __str__(self):
        return f'Coach {self.full_name}'


class Notification(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(
        'base.Session',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='coach_session_notification',
    )
    type = EnumCharField(
        enum=NotificationTypeChoices,
        default=NotificationTypeChoices.new_session,
        verbose_name=_('Type'),
        max_length=32,
        blank=True,
        null=True,
    )
    seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Notification'

    def __str__(self):
        return f'Coach {self.coach.full_name} Notification'
