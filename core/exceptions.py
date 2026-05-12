from django.core.exceptions import ValidationError


class MaxLengthValidationError(ValidationError):
    pass