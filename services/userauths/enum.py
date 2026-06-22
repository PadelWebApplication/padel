from services.enum import ChoiceEnum
from django.utils.translation import gettext_lazy as _


class UserTypeChoices(ChoiceEnum):
    coach = ('coach', _('Coach'))
    client = ('client', _('Client'))