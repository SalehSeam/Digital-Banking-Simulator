"""
validators.py
--------------
Small helper functions that check whether user input is valid
BEFORE it is used anywhere else in the app (database, GUI, etc.).

Keeping all validation logic in one file makes it easy to reuse
the same checks in the registration form, login form, and the
deposit / withdraw forms.
"""

import re

# A simple regex pattern to check for a valid-looking email address.
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def is_valid_name(name: str) -> bool:
    """Return True if the name is not empty and only contains letters/spaces."""
    name = name.strip()
    if len(name) < 2:
        return False
    # Allow letters and spaces only (simple rule for a beginner project).
    return all(char.isalpha() or char.isspace() for char in name)


def is_valid_email(email: str) -> bool:
    """Return True if the email looks like a valid email address."""
    email = email.strip()
    return re.match(EMAIL_PATTERN, email) is not None


def is_valid_pin(pin: str) -> bool:
    """Return True if the PIN is exactly 4 digits (e.g. '1234')."""
    return pin.isdigit() and len(pin) == 4


def is_valid_amount(amount_text: str) -> bool:
    """
    Return True if the given text represents a positive number.
    Used for deposit and withdraw amount fields.
    """
    try:
        amount = float(amount_text)
        return amount > 0
    except ValueError:
        return False


def get_validation_error(name: str = None, email: str = None, pin: str = None) -> str:
    """
    Check registration fields together and return the first error message found.
    Returns an empty string "" if everything is valid.
    This helper keeps the GUI code short and readable.
    """
    if name is not None and not is_valid_name(name):
        return "Please enter a valid name (letters only, at least 2 characters)."
    if email is not None and not is_valid_email(email):
        return "Please enter a valid email address."
    if pin is not None and not is_valid_pin(pin):
        return "PIN must be exactly 4 digits (e.g. 1234)."
    return ""
