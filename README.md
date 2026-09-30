# 🏦 Digital Banking Simulator

A beginner-friendly **Python + Tkinter + SQLite** desktop application that
simulates the core features of a digital bank — registration, login,
deposits, withdrawals, transaction history, and account profile.

> ⚠️ **Educational Project Disclaimer**
> This is a **simulated banking application built for learning purposes only**.
> It does **not** connect to any real bank, payment gateway, or financial API,
> and it does **not** process real money or real financial data. All account
> numbers, balances, and transactions are fictional demo data.

---

## 📌 Project Overview

Digital Banking Simulator was built as a portfolio project to demonstrate
core Python programming concepts — GUI development, database integration,
input validation, and basic authentication/security practices — through a
practical, real-world-style application.

It mimics the everyday experience of using a digital banking app: users can
register for a demo account, log in securely with a 4-digit PIN, check their
balance, deposit or withdraw money, and view their transaction history — all
running locally on SQLite with no external services required.

---

## ✨ Features

- 👤 **User Registration** — create a new demo bank account with name, email, and PIN
- 🔢 **Automatic Account Number Generation** — unique `DBS-XXXXXX` format
- 🔐 **Secure PIN Login** — 4-digit PIN, hidden input (`****`), hashed storage (never stored as plain text)
- 🚫 **Limited Failed Login Attempts** — account temporarily locks after 3 incorrect PIN attempts
- 🏠 **Dashboard** — clean overview of account and balance
- 💰 **Check Balance** — view current balance instantly
- 📥 **Deposit Money** — add funds with input validation
- 📤 **Withdraw Money** — remove funds, with **insufficient balance protection**
- 📜 **Transaction History** — full log of deposits/withdrawals with date & time
- 🧾 **Account Profile** — view name, email, account number, and join date
- 📊 **Deposit/Withdrawal Summary** — totals and counts of all transactions
- ✅ **Input Validation** — name, email, PIN, and amount fields are all validated
- 🛑 **Error Handling** — friendly error messages instead of crashes
- 🚪 **Logout** — safely return to the login screen

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3** | Core application logic |
| **Tkinter** | Graphical user interface (GUI) |
| **SQLite3** | Local database storage |
| **hashlib** | One-way PIN hashing (SHA-256) |

No external/third-party packages are required — the entire project runs on
Python's standard library.

---

## 📂 Project Structure

```text
Digital-Banking-Simulator/
├── app.py                 # Main entry point — run this file to start the app
├── database.py             # Database connection, table creation, demo data seeding
├── auth.py                  # Registration, login, PIN hashing, failed-attempt tracking
├── banking.py               # Deposit, withdraw, balance, history, summary logic
├── validators.py            # Input validation helper functions
├── gui/
│   ├── __init__.py
│   ├── theme.py              # Shared dark blue color palette & fonts
│   ├── login.py               # Login screen
│   ├── register.py            # Registration screen
│   ├── dashboard.py           # Main dashboard (balance + actions)
│   ├── transactions.py        # Transaction history screen
│   └── profile.py             # Profile & summary screen
├── database/                # SQLite database file is created here at runtime
├── assets/                  # (Optional) icons/images for the UI
├── screenshots/              # App screenshots for this README
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher installed on your machine
- Tkinter (bundled with most Python installations by default)

### Steps

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/<your-username>/Digital-Banking-Simulator.git
   cd Digital-Banking-Simulator
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(No external packages are actually required — this project only uses Python's built-in standard library.)*

---

## ▶️ How to Run

Run the application from the project's root folder:

```bash
python app.py
```

On first launch, the app automatically creates the SQLite database
(`database/banking.db`) and tables, and seeds one demo account so you can
try the app immediately.

---

## 🔑 Demo Credentials

Use these credentials to log in right away without registering:

| Field | Value |
|---|---|
| **Account Number** | `DBS-100001` |
| **PIN** | `1234` |
| **Starting Balance** | `৳10,000` (simulated) |

> This demo account is created automatically the first time the app runs.
> You can also register your own new demo account from the login screen.

---

## 🗄️ Database Explanation

The app uses a local **SQLite** database (`database/banking.db`) with two tables:

**`users`**
| Column | Description |
|---|---|
| `id` | Auto-incrementing primary key |
| `account_number` | Unique demo account number (e.g. `DBS-100001`) |
| `full_name` | User's full name |
| `email` | Unique email address |
| `pin_hash` | SHA-256 hash of the 4-digit PIN (never stored in plain text) |
| `balance` | Current account balance |
| `created_at` | Account creation timestamp |

**`transactions`**
| Column | Description |
|---|---|
| `id` | Auto-incrementing primary key |
| `account_number` | Links to the `users` table |
| `transaction_type` | `"Deposit"` or `"Withdrawal"` |
| `amount` | Transaction amount |
| `balance_after` | Balance immediately after this transaction |
| `created_at` | Timestamp of the transaction |

All database queries use **parameterized SQL statements** (`?` placeholders)
to prevent SQL injection — a basic but important security practice.

---

## 📸 Screenshots

*(Add your own screenshots here after running the app.)*

| Login | Dashboard |
|---|---|
| `screenshots/login_screen.png` | `screenshots/dashboard_screen.png` |

| Transaction History | Profile |
|---|---|
| `screenshots/transactions_screen.png` | `screenshots/profile_screen.png` |

---

## 🚀 Future Improvements

- 💸 Fund transfers between two demo accounts
- 📈 Spending charts/graphs (e.g. with `matplotlib`)
- 🌙 Light/Dark theme toggle
- 📄 Export transaction history to PDF/CSV
- 🔒 Password/PIN reset flow with security questions
- ☁️ Optional cloud sync using a real backend (for advanced learning)
- 📱 Responsive UI redesign with a modern framework (e.g. CustomTkinter)

---

## 🎓 Educational Disclaimer

This project was created **strictly for educational purposes** — to practice
Python, GUI development, database integration, and basic software design
patterns. It is **not** a real banking product, does **not** process real
money, and should **never** be used to handle real financial data or
transactions. All account numbers, balances, and personal details shown or
generated by this app are simulated.

---

## 📝 License

This project is free to use for learning and portfolio purposes.

## 👤 Author

Built by 
1. Miftahul Jannat (Dept of ITM )
2.Abu Saleh Seam   (Dept of ITM )
as a portfolio project to practice Python, software design, and GUI development.
