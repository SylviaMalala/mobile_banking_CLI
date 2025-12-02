# Mobile Banking CLI

A command-line interface banking application built with Python and SQLAlchemy that simulates a complete banking system with user management, multiple account types, transactions, and more.

## Features

### User Management

- **Create User**: Register new users with email, password, and optional full name
- **Login/Logout**: Secure authentication system
- **User Profiles**: Store user information including email, full name, phone, and account status

### Account Management

- **Multiple Account Types**: Support for Savings, Checking, and Credit accounts
- **Create Accounts**: Users can create multiple accounts with unique account numbers
- **Check Balance**: View current account balance
- **Multi-currency Support**: Accounts support different currencies (default: KES)

### Banking Operations

- **Deposit**: Add funds to any account
- **Withdraw**: Withdraw funds with balance verification
- **Transfer**: Transfer money between accounts
- **Transaction History**: View complete transaction logs with timestamps

### Data Models

The application includes the following entities:

- **User**: Customer information and authentication
- **Account**: Bank accounts with balances and types
- **Transaction**: Records of all financial operations
- **Beneficiary**: Saved recipient information for transfers
- **Card**: Credit/debit card information
- **AuditLog**: System audit trail for all actions

## Technology Stack

- **Python 3.x**
- **SQLAlchemy**: ORM for database management
- **SQLite**: Lightweight database storage (`bank.db`)
- **getpass**: Secure password input

## Database Schema

### Users Table

- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `full_name` (String, Optional)
- `phone` (String, Optional)
- `hashed_password` (String)
- `is_active` (Boolean)
- `created_at` (DateTime)

### Accounts Table

- `id` (UUID, Primary Key)
- `owner_id` (UUID, Foreign Key → Users)
- `account_number` (String, Unique)
- `type` (Enum: savings/checking/credit)
- `balance` (Decimal)
- `currency` (String)
- `created_at` (DateTime)

### Transactions Table

- `id` (UUID, Primary Key)
- `account_id` (UUID, Foreign Key → Accounts)
- `amount` (Decimal)
- `type` (Enum: deposit/withdrawal/transfer/fee)
- `reference` (String)
- `created_at` (DateTime)

### Additional Tables

- **Beneficiaries**: Store frequent transfer recipients
- **Cards**: Manage user payment cards
- **AuditLogs**: Track all system actions

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SylviaMalala/mobile_banking_CLI.git
cd mobile_banking_CLI
```

2. Install dependencies:

```bash
pip install sqlalchemy
```

3. Run the application:

```bash
python app.py
```

## Usage

### Main Menu Options

```text
=== Welcome to CLI Bank ===
1. Create user
2. Login
3. Exit
```

### User Menu Options

```text
=== Hello, [User] ===
1. Create account
2. Check balance
3. Deposit
4. Withdraw
5. Transfer
6. Transaction history
7. Logout
```

### Example Workflow

1. **Create a User**:
   - Select option 1 from the main menu
   - Enter email, password, and full name

2. **Login**:
   - Select option 2 from the main menu
   - Enter your credentials

3. **Create an Account**:
   - From user menu, select option 1
   - Enter account number and choose account type

4. **Make a Deposit**:
   - Select option 3
   - Choose your account
   - Enter amount to deposit

5. **Transfer Money**:
   - Select option 5
   - Choose source account
   - Enter recipient account number
   - Enter transfer amount

6. **View Transaction History**:
   - Select option 6
   - Choose account to view history

## File Structure

```text
mobile_banking_CLI/
├── app.py          # Main application with CLI interface and banking operations
├── models.py       # SQLAlchemy models and database configuration
├── README.md       # Project documentation
└── bank.db         # SQLite database (created automatically)
```

## Features in Detail

### Transaction Types

- **Deposit**: Add money to an account
- **Withdrawal**: Remove money from an account (with balance check)
- **Transfer**: Move money between accounts (creates two transactions)
- **Fee**: Record banking fees

### Account Types

- **Savings**: Standard savings account
- **Checking**: Everyday transaction account
- **Credit**: Credit line account

### Security Features

- Password masking using `getpass`
- Email-based unique user identification
- Balance verification before withdrawals and transfers
- Transaction logging for audit trail

## Database

The application uses SQLite with the following features:

- Automatic table creation on first run
- UUID-based primary keys for better scalability
- Cascading deletes for referential integrity
- Timestamps for all records
- Decimal precision for monetary amounts

## Future Enhancements

Potential features for future development:

- Password hashing (currently stores plain text)
- Beneficiary management UI
- Card management functionality
- Interest calculation for savings accounts
- Transaction fees
- Account statements and reports
- Multi-user sessions
- REST API integration

## Author

Sylvia Malala

## License

This project is open source and available for educational purposes.

---

© 2025 Sylvia Malala. All rights reserved.
