"""
database.py
------------
Handles everything related to the SQLite database:
- Creating the database file and tables
- Providing a single connection function used by the rest of the app
- Inserting demo/sample data the first time the app runs

The database file is stored inside the "database" folder so all
project data stays organized in one place.
"""

import sqlite3
import os
import hashlib

# Path to the SQLite database file.
DB_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
DB_PATH = os.path.join(DB_FOLDER, "banking.db")

# Demo account details (simulated / educational only — see README).
DEMO_ACCOUNT_NUMBER = "DBS-100001"
DEMO_PIN = "1234"
DEMO_BALANCE = 10000.0
DEMO_NAME = "Demo User"
DEMO_EMAIL = "demo@example.com"


def hash_pin(pin: str) -> str:
    """
    Turn a 4-digit PIN into a secure hash before storing it.
    We NEVER store the plain PIN in the database.
    SHA-256 is a one-way hash, so the original PIN cannot be recovered from it.
    """
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def get_connection() -> sqlite3.Connection:
    """
    Create (if needed) and return a connection to the SQLite database.
    Every function that needs the database calls this to get a connection.
    """
    os.makedirs(DB_FOLDER, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    # Let us access columns by name, e.g. row["balance"] instead of row[2].
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """
    Create the "users" and "transactions" tables if they do not already exist,
    and insert one demo account so the app can be tested immediately.
    This function is safe to call every time the app starts.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Table that stores each user's account information.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            pin_hash TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table that stores every deposit / withdrawal made by users.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            balance_after REAL NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_number) REFERENCES users (account_number)
        )
    """)

    connection.commit()

    # Insert the demo account only if it does not already exist.
    cursor.execute(
        "SELECT * FROM users WHERE account_number = ?", (DEMO_ACCOUNT_NUMBER,)
    )
    if cursor.fetchone() is None:
        cursor.execute(
            """
            INSERT INTO users (account_number, full_name, email, pin_hash, balance)
            VALUES (?, ?, ?, ?, ?)
            """,
            (DEMO_ACCOUNT_NUMBER, DEMO_NAME, DEMO_EMAIL, hash_pin(DEMO_PIN), DEMO_BALANCE),
        )
        connection.commit()

        # Give the demo account one starting transaction so history isn't empty.
        cursor.execute(
            """
            INSERT INTO transactions (account_number, transaction_type, amount, balance_after)
            VALUES (?, ?, ?, ?)
            """,
            (DEMO_ACCOUNT_NUMBER, "Initial Deposit (Demo)", DEMO_BALANCE, DEMO_BALANCE),
        )
        connection.commit()

    connection.close()
