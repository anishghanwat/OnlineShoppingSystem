"""Validation utilities for the application."""
from backend.utils.exceptions import ValidationException


def validate_positive_number(value: float, field_name: str = "Value") -> None:
    """Validate that a number is positive."""
    if value <= 0:
        raise ValidationException(f"{field_name} must be positive")


def validate_positive_integer(value: int, field_name: str = "Value") -> None:
    """Validate that an integer is positive."""
    if not isinstance(value, int) or value <= 0:
        raise ValidationException(f"{field_name} must be a positive integer")


def validate_non_negative_integer(value: int, field_name: str = "Value") -> None:
    """Validate that an integer is non-negative."""
    if not isinstance(value, int) or value < 0:
        raise ValidationException(f"{field_name} must be a non-negative integer")


def validate_email(email: str) -> None:
    """Basic email validation."""
    if not email or "@" not in email or "." not in email:
        raise ValidationException("Invalid email format")


def validate_string_length(value: str, min_length: int = 1, max_length: int = 255, field_name: str = "Field") -> None:
    """Validate string length."""
    if not value or len(value) < min_length:
        raise ValidationException(f"{field_name} must be at least {min_length} characters")
    if len(value) > max_length:
        raise ValidationException(f"{field_name} must be at most {max_length} characters")
