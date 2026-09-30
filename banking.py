"""
banking.py
-----------
Core banking operations that work on an already logged-in account:
- Checking balance
- Depositing money
- Withdrawing money (with insufficient-funds protection)
- Reading transaction history
- Calculating total deposit / withdrawal summary

All database access here uses parameterized queries ("?" placeholders)
to avoid SQL injection, which is a basic but important security practice.
"""

from database import get_connection


def get_balance(account_number: str) -> float:
    """Return the current balance for the given account."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT balance FROM users WHERE account_number = ?", (account_number,)
    )
    row = cursor.fetchone()
    connection.close()
    return row["balance"] if row else 0.0


def deposit(account_number: str, amount: float) -> tuple[bool, str]:
    """
    Add money to the account and record the transaction.
    Returns (success, message).
    """
    if amount <= 0:
        return False, "Deposit amount must be greater than zero."

    connection = get_connection()
    cursor = connection.cursor()

    new_balance = get_balance(account_number) + amount

    cursor.execute(
        "UPDATE users SET balance = ? WHERE account_number = ?",
        (new_balance, account_number),
    )
    cursor.execute(
        """
        INSERT INTO transactions (account_number, transaction_type, amount, balance_after)
        VALUES (?, 'Deposit', ?, ?)
        """,
        (account_number, amount, new_balance),
    )
    connection.commit()
    connection.close()
    return True, f"Deposit successful. New balance: {new_balance:,.2f}"


def withdraw(account_number: str, amount: float) -> tuple[bool, str]:
    """
    Remove money from the account, but only if there is enough balance.
    Returns (success, message).
    """
    if amount <= 0:
        return False, "Withdrawal amount must be greater than zero."

    current_balance = get_balance(account_number)

    # Prevent withdrawal when balance is insufficient.
    if amount > current_balance:
        return False, "Insufficient balance for this withdrawal."

    new_balance = current_balance - amount

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE users SET balance = ? WHERE account_number = ?",
        (new_balance, account_number),
    )
    cursor.execute(
        """
        INSERT INTO transactions (account_number, transaction_type, amount, balance_after)
        VALUES (?, 'Withdrawal', ?, ?)
        """,
        (account_number, amount, new_balance),
    )
    connection.commit()
    connection.close()
    return True, f"Withdrawal successful. New balance: {new_balance:,.2f}"


def get_transaction_history(account_number: str) -> list:
    """Return all transactions for this account, newest first."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT transaction_type, amount, balance_after, created_at
        FROM transactions
        WHERE account_number = ?
        ORDER BY created_at DESC, id DESC
        """,
        (account_number,),
    )
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_summary(account_number: str) -> dict:
    """
    Return a dictionary with total deposits, total withdrawals,
    and how many transactions of each type were made.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS count
        FROM transactions
        WHERE account_number = ? AND transaction_type = 'Deposit'
        """,
        (account_number,),
    )
    deposit_row = cursor.fetchone()

    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS count
        FROM transactions
        WHERE account_number = ? AND transaction_type = 'Withdrawal'
        """,
        (account_number,),
    )
    withdrawal_row = cursor.fetchone()

    connection.close()

    return {
        "total_deposits": deposit_row["total"],
        "deposit_count": deposit_row["count"],
        "total_withdrawals": withdrawal_row["total"],
        "withdrawal_count": withdrawal_row["count"],
    }
