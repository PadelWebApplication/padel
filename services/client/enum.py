from services.enum import ChoiceEnum
from django.utils.translation import gettext_lazy as _


class NotificationTypeChoices(ChoiceEnum):
    session_scheduled = ('session_scheduled', _('Session Scheduled'))
    session_cancelled = ('session_cancelled', _('Session Cancelled'))
