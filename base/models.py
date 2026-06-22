from django.db import models
from django.utils.translation import gettext_lazy as _

from shortuuid.django_fields import ShortUUIDField
from django_enum.fields import EnumCharField

from coach import models as coach_models
from client import models as client_models
from services.base.enum import SessionStatusChoices, BillingStatusChoices
from core.db import AbstractCreatedByUpdatedByModel


class Service(AbstractCreatedByUpdatedByModel):
    image = models.FileField(upload_to='images', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_coaches = models.ManyToManyField(coach_models.Coach, blank=True)

    def __str__(self):
        return f'{self.name} - {self.cost}'


class Session(AbstractCreatedByUpdatedByModel):
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_sessions',
    )
    coach = models.ForeignKey(
        coach_models.Coach,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coach_sessions',
    )
    client = models.ForeignKey(
        client_models.Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions_client',
    )
    session_date = models.DateTimeField(null=True, blank=True)
    session_id = ShortUUIDField(length=6, max_length=10, alphabet='1234567890')
    status = EnumCharField(
        enum=SessionStatusChoices,
        default=SessionStatusChoices.scheduled,
        verbose_name=_('Status'),
        max_length=16,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.client.full_name} with {self.coach.full_name}"
    
class SessionNote(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name="notes")
    summary = models.TextField(help_text="What was discussed?")
    client_mindset = models.TextField(blank=True, null=True)
    coach_observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Notes for {self.session.client.full_name}"

class ActionItem(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="action_items")
    task = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Task for {self.session.client.full_name}: {self.task[:20]}"

class Resource(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="resources/", blank=True, null=True)

    def __str__(self):
        return self.title


class Billing(AbstractCreatedByUpdatedByModel):
    client = models.ForeignKey(
        client_models.Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='billings',
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='billing', blank=True, null=True
    )
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = EnumCharField(
        enum=BillingStatusChoices,
        default=BillingStatusChoices.unpaid,
        verbose_name=_('Status'),
        max_length=16,
        blank=True,
        null=True,
    )
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet='1234567890')

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Billing for {self.client.full_name} - Total: {self.total}'
