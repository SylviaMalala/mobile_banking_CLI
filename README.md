# Mobile Banking CLI

A command-line interface banking application built with Python and SQLAlchemy that simulates a complete banking system with user management, multiple account types, transactions, and more.

## 🚀 Features

### User Management

- **Create User**: Register new users with email, password, and optional full name
- **Login/Logout**: Secure authentication with password masking
- **User Profiles**: Store user information including email, full name, phone, and account status
- **Multi-user Support**: Multiple users can have accounts in the system

### Account Management

- **Multiple Account Types**: Support for Savings, Checking, and Credit accounts
- **Create Accounts**: Users can create multiple accounts with unique account numbers
- **Check Balance**: View current account balance in real-time
- **Multi-currency Support**: Accounts support different currencies (default: KES)
- **Account Selection**: Easy account selection interface for operations

### Banking Operations

- **Deposit**: Add funds to any account with instant balance updates
- **Withdraw**: Withdraw funds with automatic balance verification
- **Transfer**: Transfer money between accounts with dual transaction logging
- **Transaction History**: View complete transaction logs with timestamps, types, and references
- **Transaction Types**: Support for deposits, withdrawals, transfers, and fees

### Data Models

The application includes the following entities:

- **User**: Customer information and authentication
- **Account**: Bank accounts with balances and types (Checking, Savings, Credit)
- **Transaction**: Complete records of all financial operations
- **Beneficiary**: Saved recipient information for quick transfers
- **Card**: Credit/debit card information management
- **AuditLog**: System-wide audit trail for all actions

## 🛠️ Technology Stack

- **Python 3.12+**: Modern Python with type hints
- **SQLAlchemy 2.0+**: Advanced ORM with modern features
- **SQLite**: Lightweight, embedded database
- **UUID**: Secure unique identifiers for all entities
- **Decimal**: Precise financial calculations
- **Virtual Environment**: Isolated dependency management



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

1. Create a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate  # On Windows
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Run the application:

```bash
python app.py
```

**Note**: If using a virtual environment, make sure it's activated before running the app.

## 🧪 Testing with Sample Data

To quickly test the application with pre-populated data:

```bash
python seed_data.py
```

This will create 5 test users with accounts, transactions, beneficiaries, and cards. Test credentials:

- `sylvia.malala@example.com` / `password123`
- `mathew.august@example.com` / `password123`
- `test@test.com` / `test123`

## 📖 Usage

### Main Menu Options

```text
=== Welcome to CLI Bank ===
1. Create user
2. Login
3. Exit
```

### Example Workflow

#### First-Time Setup

1. **Create a User**:
   - Select option `1` from the main menu
   - Enter email, password, and full name (optional)

2. **Login**:
   - Select option `2` from the main menu
   - Enter your credentials

3. **Create an Account**:
   - From user menu, select option `1`
   - Enter unique account number (e.g., ACC001234567890)
   - Choose account type: savings, checking, or credit

#### Daily Operations

1. **Make a Deposit**:
   - Select option `3` from user menu
   - Choose your account from the list
   - Enter amount to deposit

2. **Withdraw Funds**:
   - Select option `4` from user menu
   - Choose your account
   - Enter withdrawal amount (verified against balance)

3. **Transfer Money**:
   - Select option `5` from user menu
   - Choose source account
   - Enter recipient account number
   - Enter transfer amount
   - System creates transactions for both accounts

4. **View Transaction History**:
   - Select option `6` from user menu
   - Choose account to view history
   - See all deposits, withdrawals, transfers, and fees

## 📁 Project Structure

```text
mobile_banking_CLI/
├── app.py              # Main CLI application with user interface and banking operations
├── models.py           # SQLAlchemy ORM models and database schema
├── seed_data.py        # Database seeding script with test data
├── config.py           # Configuration settings and environment variables
├── requirements.txt    # Python package dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Contribution guidelines
## 🔒 Security Features

- **Password Masking**: Input masking using `getpass` module for secure credential entry
- **Unique Email Authentication**: Email-based unique user identification
- **Balance Verification**: Automatic balance checks before withdrawals and transfers
- **Transaction Logging**: Complete audit trail for all financial operations
- **UUID-based IDs**: Secure, non-sequential identifiers for all entities
- **Session Management**: Proper database session handling with context managers

## 💡 Key Implementation Details

### Transaction Types

- **DEPOSIT**: Add money to an account with instant balance update
- **WITHDRAWAL**: Remove money from an account (with automatic balance verification)
- **TRANSFER**: Move money between accounts (creates two transactions for complete audit trail)
- **FEE**: Record banking fees and charges

### Account Types

- **SAVINGS**: Standard savings account for long-term storage
- **CHECKING**: Everyday transaction account for regular use
- **CREDIT**: Credit line account for lending operations

### Database Features

- **Relationships**: Proper foreign key relationships between all entities
- **Cascading Deletes**: Automatic cleanup of related records
- **Timestamps**: Automatic creation timestamps on all records
- **Decimal Precision**: 18,2 precision for all monetary values
- **Enum Types**: Type-safe account and transaction types
### Account Types

- **Savings**: Standard savings account
## 🗄️ Database

The application uses SQLite with the following features:

- **Automatic Schema Creation**: Tables created automatically on first run
- **UUID Primary Keys**: Better scalability and security
- **Referential Integrity**: Foreign key constraints with cascading deletes
- **Automatic Timestamps**: Created_at fields on all records
- **Decimal Precision**: 18,2 precision for all monetary amounts
- **Type Safety**: Enum types for account and transaction types
- **Session Management**: Context managers for proper connection handling

### Database Location

- Default: `./bank.db` in project root
- Configurable via `DATABASE_URL` environment variable in `.env` file

## Database

The application uses SQLite with the following features:
## 🔮 Future Enhancements

Potential features for future development:

- [ ] **Password Hashing**: Implement bcrypt or argon2 for secure password storage
- [ ] **Beneficiary Management UI**: Add/edit/delete beneficiaries through CLI
- [ ] **Card Management**: Activate/deactivate cards, view card details
- [ ] **Interest Calculation**: Automatic interest accrual for savings accounts
- [ ] **Transaction Fees**: Configurable fee structure for different operations
- [ ] **Account Statements**: Generate periodic account statements
- [ ] **Export Features**: Export transactions to CSV/PDF
- [ ] **Multi-factor Authentication**: Enhanced security with 2FA
- [ ] **REST API**: Web service API for mobile/web clients
- [ ] **Rate Limiting**: Prevent abuse with request throttling
- [ ] **Email Notifications**: Transaction alerts and statements
- [ ] **Loan Management**: Loan application and repayment tracking

## 🧪 Development & Testing

### Running Tests
## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Sylvia Malala**

- GitHub: [@SylviaMalala](https://github.com/SylviaMalala)
- Project: [mobile_banking_CLI](https://github.com/SylviaMalala/mobile_banking_CLI)

## 🙏 Acknowledgments

- Built with SQLAlchemy ORM
- Inspired by modern banking systems
- Created for educational purposes

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**© 2025 Sylvia Malala. All rights reserved.**
### Development Mode

To enable SQL query logging, set in `config.py`:

```python
DEBUG = True  # or set DEBUG=True in .env file
```

This will show all SQL queries in the console output.

## 🤝 Contributing

## License

This project is open source and available for educational purposes.

---

© 2025 Sylvia Malala. All rights reserved.
