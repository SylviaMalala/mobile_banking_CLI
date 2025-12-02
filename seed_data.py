"""
Seed script to populate the database with test data.
Run this script to add sample users, accounts, and transactions for testing.
"""
from decimal import Decimal
from datetime import datetime, timedelta
from models import (
    Session,
    User,
    Account,
    Transaction,
    Beneficiary,
    Card,
    AuditLog,
    AccountType,
    TransactionType,
    gen_uuid
)

def clear_all_data():
    """Clear all existing data from the database."""
    with Session() as session:
        session.query(Transaction).delete()
        session.query(Beneficiary).delete()
        session.query(Card).delete()
        session.query(Account).delete()
        session.query(AuditLog).delete()
        session.query(User).delete()
        session.commit()
        print("✓ Cleared all existing data")

def create_users():
    """Create sample users."""
    users_data = [
        {
            "email": "sylvia.malala@example.com",
            "full_name": "Sylvia Malala",
            "phone": "+254712345678",
            "hashed_password": "password123"
        },
        {
            "email": "mathew.august@example.com",
            "full_name": "Mathew August",
            "phone": "+254723456789",
            "hashed_password": "password123"
        },
        {
            "email": "bob.wilson@example.com",
            "full_name": "Bob Wilson",
            "phone": "+254734567890",
            "hashed_password": "password123"
        },
        {
            "email": "alice.johnson@example.com",
            "full_name": "Alice Johnson",
            "phone": "+254745678901",
            "hashed_password": "password123"
        },
        {
            "email": "test@test.com",
            "full_name": "Test User",
            "phone": "+254756789012",
            "hashed_password": "test123"
        }
    ]
    
    users = []
    with Session() as session:
        for user_data in users_data:
            user = User(
                id=gen_uuid(),
                email=user_data["email"],
                full_name=user_data["full_name"],
                phone=user_data["phone"],
                hashed_password=user_data["hashed_password"],
                is_active=True
            )
            session.add(user)
            users.append(user)
        
        session.commit()
        print(f"✓ Created {len(users)} users")
        return [u.id for u in users]

def create_accounts(user_ids):
    """Create sample accounts for users."""
    accounts_data = [
        # Sylvia Malala's accounts
        {"owner_id": user_ids[0], "account_number": "ACC001234567890", "type": AccountType.CHECKING, "balance": Decimal("50000.00")},
        {"owner_id": user_ids[0], "account_number": "SAV001234567890", "type": AccountType.SAVINGS, "balance": Decimal("150000.00")},
        
        # Mathew August's accounts
        {"owner_id": user_ids[1], "account_number": "ACC002345678901", "type": AccountType.CHECKING, "balance": Decimal("75000.00")},
        {"owner_id": user_ids[1], "account_number": "SAV002345678901", "type": AccountType.SAVINGS, "balance": Decimal("200000.00")},
        {"owner_id": user_ids[1], "account_number": "CRD002345678901", "type": AccountType.CREDIT, "balance": Decimal("0.00")},
        
        # Bob Wilson's accounts
        {"owner_id": user_ids[2], "account_number": "ACC003456789012", "type": AccountType.CHECKING, "balance": Decimal("30000.00")},
        {"owner_id": user_ids[2], "account_number": "SAV003456789012", "type": AccountType.SAVINGS, "balance": Decimal("100000.00")},
        
        # Alice Johnson's accounts
        {"owner_id": user_ids[3], "account_number": "ACC004567890123", "type": AccountType.CHECKING, "balance": Decimal("45000.00")},
        
        # Test User's accounts
        {"owner_id": user_ids[4], "account_number": "ACC005678901234", "type": AccountType.CHECKING, "balance": Decimal("10000.00")},
        {"owner_id": user_ids[4], "account_number": "SAV005678901234", "type": AccountType.SAVINGS, "balance": Decimal("25000.00")},
    ]
    
    accounts = []
    with Session() as session:
        for acc_data in accounts_data:
            account = Account(
                id=gen_uuid(),
                owner_id=acc_data["owner_id"],
                account_number=acc_data["account_number"],
                type=acc_data["type"],
                balance=acc_data["balance"],
                currency="KES"
            )
            session.add(account)
            accounts.append(account)
        
        session.commit()
        print(f"✓ Created {len(accounts)} accounts")
        return [a.id for a in accounts]

def create_transactions(account_ids):
    """Create sample transactions."""
    transactions_data = [
        # Deposits
        {"account_id": account_ids[0], "amount": Decimal("10000.00"), "type": TransactionType.DEPOSIT, "reference": "Salary deposit"},
        {"account_id": account_ids[0], "amount": Decimal("5000.00"), "type": TransactionType.DEPOSIT, "reference": "Freelance payment"},
        {"account_id": account_ids[2], "amount": Decimal("20000.00"), "type": TransactionType.DEPOSIT, "reference": "Monthly salary"},
        {"account_id": account_ids[4], "amount": Decimal("15000.00"), "type": TransactionType.DEPOSIT, "reference": "Bonus payment"},
        
        # Withdrawals
        {"account_id": account_ids[0], "amount": Decimal("2000.00"), "type": TransactionType.WITHDRAWAL, "reference": "ATM withdrawal"},
        {"account_id": account_ids[2], "amount": Decimal("5000.00"), "type": TransactionType.WITHDRAWAL, "reference": "Cash withdrawal"},
        {"account_id": account_ids[5], "amount": Decimal("3000.00"), "type": TransactionType.WITHDRAWAL, "reference": "Grocery shopping"},
        
        # Transfers
        {"account_id": account_ids[0], "amount": Decimal("8000.00"), "type": TransactionType.TRANSFER, "reference": "Transfer to savings"},
        {"account_id": account_ids[1], "amount": Decimal("8000.00"), "type": TransactionType.DEPOSIT, "reference": "Transfer from checking"},
        {"account_id": account_ids[2], "amount": Decimal("12000.00"), "type": TransactionType.TRANSFER, "reference": "Rent payment"},
        {"account_id": account_ids[7], "amount": Decimal("12000.00"), "type": TransactionType.DEPOSIT, "reference": "Rent received"},
        
        # Fees
        {"account_id": account_ids[0], "amount": Decimal("50.00"), "type": TransactionType.FEE, "reference": "Monthly maintenance fee"},
        {"account_id": account_ids[2], "amount": Decimal("50.00"), "type": TransactionType.FEE, "reference": "Monthly maintenance fee"},
        {"account_id": account_ids[5], "amount": Decimal("25.00"), "type": TransactionType.FEE, "reference": "ATM fee"},
    ]
    
    with Session() as session:
        for i, trans_data in enumerate(transactions_data):
            transaction = Transaction(
                id=gen_uuid(),
                account_id=trans_data["account_id"],
                amount=trans_data["amount"],
                type=trans_data["type"],
                reference=trans_data["reference"]
            )
            session.add(transaction)
        
        session.commit()
        print(f"✓ Created {len(transactions_data)} transactions")

def create_beneficiaries(user_ids):
    """Create sample beneficiaries."""
    beneficiaries_data = [
        {"owner_id": user_ids[0], "name": "Mathew August", "account_number": "ACC002345678901", "bank_name": "CLI Bank"},
        {"owner_id": user_ids[0], "name": "Electric Company", "account_number": "UTL111222333444", "bank_name": "Utility Bank"},
        {"owner_id": user_ids[1], "name": "Bob Wilson", "account_number": "ACC003456789012", "bank_name": "CLI Bank"},
        {"owner_id": user_ids[1], "name": "Internet Provider", "account_number": "ISP999888777666", "bank_name": "Service Bank"},
        {"owner_id": user_ids[2], "name": "Alice Johnson", "account_number": "ACC004567890123", "bank_name": "CLI Bank"},
        {"owner_id": user_ids[4], "name": "Mom", "account_number": "FAM123456789012", "bank_name": "Family Bank"},
    ]
    
    with Session() as session:
        for ben_data in beneficiaries_data:
            beneficiary = Beneficiary(
                id=gen_uuid(),
                owner_id=ben_data["owner_id"],
                name=ben_data["name"],
                account_number=ben_data["account_number"],
                bank_name=ben_data["bank_name"]
            )
            session.add(beneficiary)
        
        session.commit()
        print(f"✓ Created {len(beneficiaries_data)} beneficiaries")

def create_cards(user_ids):
    """Create sample cards."""
    cards_data = [
        {"owner_id": user_ids[0], "card_mask": "4532-****-****-1234", "last4": "1234", "expiry_month": 12, "expiry_year": 2027},
        {"owner_id": user_ids[0], "card_mask": "5425-****-****-5678", "last4": "5678", "expiry_month": 6, "expiry_year": 2026},
        {"owner_id": user_ids[1], "card_mask": "4916-****-****-9012", "last4": "9012", "expiry_month": 9, "expiry_year": 2028},
        {"owner_id": user_ids[2], "card_mask": "4024-****-****-3456", "last4": "3456", "expiry_month": 3, "expiry_year": 2027},
        {"owner_id": user_ids[3], "card_mask": "5520-****-****-7890", "last4": "7890", "expiry_month": 11, "expiry_year": 2026},
        {"owner_id": user_ids[4], "card_mask": "4532-****-****-2468", "last4": "2468", "expiry_month": 8, "expiry_year": 2029},
    ]
    
    with Session() as session:
        for card_data in cards_data:
            card = Card(
                id=gen_uuid(),
                owner_id=card_data["owner_id"],
                card_mask=card_data["card_mask"],
                last4=card_data["last4"],
                expiry_month=card_data["expiry_month"],
                expiry_year=card_data["expiry_year"],
                is_active=True
            )
            session.add(card)
        
        session.commit()
        print(f"✓ Created {len(cards_data)} cards")

def create_audit_logs():
    """Create sample audit logs."""
    audit_data = [
        {"entity": "User", "entity_id": "user-001", "action": "CREATE", "payload": "User sylvia.malala@example.com created"},
        {"entity": "Account", "entity_id": "acc-001", "action": "CREATE", "payload": "Account ACC001234567890 created"},
        {"entity": "Transaction", "entity_id": "trans-001", "action": "CREATE", "payload": "Deposit of 10000.00 processed"},
        {"entity": "User", "entity_id": "user-002", "action": "LOGIN", "payload": "User mathew.august@example.com logged in"},
        {"entity": "Transaction", "entity_id": "trans-002", "action": "CREATE", "payload": "Transfer of 8000.00 processed"},
        {"entity": "Account", "entity_id": "acc-002", "action": "UPDATE", "payload": "Balance updated for account SAV001234567890"},
        {"entity": "Card", "entity_id": "card-001", "action": "CREATE", "payload": "Card ending in 1234 issued"},
        {"entity": "Beneficiary", "entity_id": "ben-001", "action": "CREATE", "payload": "Beneficiary Mathew August added"},
    ]
    
    with Session() as session:
        for audit in audit_data:
            log = AuditLog(
                entity=audit["entity"],
                entity_id=audit["entity_id"],
                action=audit["action"],
                payload=audit["payload"]
            )
            session.add(log)
        
        session.commit()
        print(f"✓ Created {len(audit_data)} audit logs")

def main():
    """Main function to seed all data."""
    print("\n" + "="*50)
    print("  DATABASE SEEDING - Test Data Generation")
    print("="*50 + "\n")
    
    # Ask for confirmation
    response = input("This will clear all existing data and create new test data. Continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Seeding cancelled.")
        return
    
    print("\nStarting database seeding...\n")
    
    # Clear existing data
    clear_all_data()
    
    # Create test data
    user_ids = create_users()
    account_ids = create_accounts(user_ids)
    create_transactions(account_ids)
    create_beneficiaries(user_ids)
    create_cards(user_ids)
    create_audit_logs()
    
    print("\n" + "="*50)
    print("  ✓ Database seeding completed successfully!")
    print("="*50)
    print("\nTest credentials:")
    print("  Email: sylvia.malala@example.com | Password: password123")
    print("  Email: mathew.august@example.com | Password: password123")
    print("  Email: test@test.com | Password: test123")
    print("\n")

if __name__ == "__main__":
    main()
