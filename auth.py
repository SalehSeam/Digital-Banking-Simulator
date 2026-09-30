"""
auth.py
--------
Everything related to user identity:
- Registering a new demo account
- Generating a unique demo account number
- Logging in with an account number + 4-digit PIN
- Keeping track of failed login attempts (basic security practice)

This is a SIMULATION. No real banking authentication standards are used.
"""

import random
import sqlite3

from database import get_connection, hash_pin

# How many wrong PIN attempts are allowed before the login is temporarily blocked.
MAX_FAILED_ATTEMPTS = 3

# Keeps track of failed attempts per account for the current app session.
# Example: {"DBS-100001": 2}
_failed_attempts = {}


def generate_account_number() -> str:
    """
    Create a new, unique demo account number in the format DBS-XXXXXX.
    Keeps generating a random number until it finds one not already used.
    """
    connection = get_connection()
    cursor = connection.cursor()

    while True:
        random_digits = random.randint(100000, 999999)
        candidate = f"DBS-{random_digits}"

        cursor.execute(
            "SELECT 1 FROM users WHERE account_number = ?", (candidate,)
        )
        if cursor.fetchone() is None:
            connection.close()
            return candidate


def register_user(full_name: str, email: str, pin: str) -> tuple[bool, str]:
    """
    Create a new user account.
    Returns (success, message_or_account_number).
    On success, message_or_account_number contains the new account number.
    On failure, it contains an error message.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Email must be unique.
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    if cursor.fetchone() is not None:
        connection.close()
        return False, "An account with this email already exists."

    account_number = generate_account_number()
    pin_hash = hash_pin(pin)

    try:
        cursor.execute(
            """
            INSERT INTO users (account_number, full_name, email, pin_hash, balance)
            VALUES (?, ?, ?, ?, ?)
            """,
            (account_number, full_name.strip(), email.strip(), pin_hash, 0.0),
        )
        connection.commit()
    except sqlite3.IntegrityError:
        connection.close()
        return False, "Could not create account. Please try again."

    connection.close()
    return True, account_number


def login_user(account_number: str, pin: str) -> tuple[bool, str]:
    """
    Try to log a user in with their account number and PIN.
    Returns (success, message).
    Tracks failed attempts per account number and blocks further tries
    once MAX_FAILED_ATTEMPTS is reached (until the app is restarted).
    """
    account_number = account_number.strip()

    # If this account already hit the limit, refuse immediately.
    if _failed_attempts.get(account_number, 0) >= MAX_FAILED_ATTEMPTS:
        return False, "Account locked due to too many failed attempts. Restart the app to try again."

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE account_number = ?", (account_number,)
    )
    user = cursor.fetchone()
    connection.close()

    if user is None:
        return False, "Account number not found."

    if user["pin_hash"] != hash_pin(pin):
        _failed_attempts[account_number] = _failed_attempts.get(account_number, 0) + 1
        remaining = MAX_FAILED_ATTEMPTS - _failed_attempts[account_number]

        if remaining <= 0:
            return False, "Incorrect PIN. Account locked due to too many failed attempts."
        return False, f"Incorrect PIN. {remaining} attempt(s) remaining."

    # Successful login resets the failed attempt counter.
    _failed_attempts[account_number] = 0
    return True, "Login successful."


def get_user_by_account(account_number: str):
    """Return the full user row for the given account number, or None."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE account_number = ?", (account_number,)
    )
    user = cursor.fetchone()
    connection.close()
    return user
