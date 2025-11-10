"""
Core validators
"""
from django.core.exceptions import ValidationError


def validate_email(email: str) -> None:
    """Validate email format"""
    if '@' not in email:
        raise ValidationError("Invalid email format")
