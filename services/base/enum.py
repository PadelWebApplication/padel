from services.enum import ChoiceEnum
from django.utils.translation import gettext_lazy as _


class SessionStatusChoices(ChoiceEnum):
    scheduled = ('scheduled', _('Scheduled'))
    completed = ('completed', _('Completed'))
    cancelled = ('cancelled', _('Cancelled'))
    pending = ('pending', _('Pending'))
