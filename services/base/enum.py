from services.enum import ChoiceEnum
from django.utils.translation import gettext_lazy as _


class ServiceTypeChoices(ChoiceEnum):
    event = ('event', _('Event'))
    camp = ('camp', _('Camp'))


class SessionStatusChoices(ChoiceEnum):
    scheduled = ('scheduled', _('Scheduled'))
    completed = ('completed', _('Completed'))
    cancelled = ('cancelled', _('Cancelled'))
    pending = ('pending', _('Pending'))


class BillingStatusChoices(ChoiceEnum):
    paid = ('paid', _('Paid'))
    reserved = ('reserved', _('Reserved'))
    unpaid = ('unpaid', _('Unpaid'))
