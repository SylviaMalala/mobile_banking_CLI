import getpass
from decimal import Decimal
from models import (
    Session,
    engine,
    User,
    Account,
    Transaction,
    AccountType,
    TransactionType,
    gen_uuid
)

def main_menu():
    while True:
        print("\n=== Welcome to CLI Bank ===")
        print("1. Create user")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            create_user_menu()
        elif choice == "2":
            user = login_menu()
            if user:
                user_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def create_user_menu():
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    full_name = input("Full Name (optional): ")
    phone = input("Phone (optional): ")
    with Session() as session:
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            print("User already exists!")
            return

        user = User(
            id=gen_uuid(),
            email=email,
            phone=phone,
            hashed_password=password,
            full_name=full_name
        )
        session.add(user)
        session.commit()
        print(f"User '{email}' created successfully!")

def login_menu():
    email = input("Email: ")
    password = getpass.getpass("Password: ")

    with Session() as session:
        user = session.query(User).filter_by(email=email, hashed_password=password).first()
        if user:
            print(f"Welcome {user.full_name or user.email}!")
            return user
        else:
            print("Invalid credentials.")
            return None

def user_menu(user):
    while True:
        print(f"\n=== Hello, {user.full_name or user.email} ===")
        print("1. Create account")
        print("2. Check balance")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. Transaction history")
        print("7. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            create_account_menu(user)
        elif choice == "2":
            check_balance(user)
        elif choice == "3":
            deposit(user)
        elif choice == "4":
            withdraw(user)
        elif choice == "5":
            transfer(user)
        elif choice == "6":
            transaction_history(user)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")

def create_account_menu(user):
    acc_number = input("Enter new account number: ")
    acc_type_input = input("Account type (savings/checking/credit) [checking]: ").lower()
    acc_type = AccountType(acc_type_input) if acc_type_input in AccountType._value2member_map_ else AccountType.CHECKING

    with Session() as session:
        account = Account(
            id=gen_uuid(),
            owner_id=user.id,
            account_number=acc_number,
            type=acc_type,
            balance=Decimal("0.00")
        )
        session.add(account)
        session.commit()
        print(f"{acc_type.value.title()} account '{acc_number}' created!")

def select_account(user):
    with Session() as session:
        accounts = session.query(Account).filter_by(owner_id=user.id).all()
        if not accounts:
            print("No accounts found. Please create an account first.")
            return None

        print("Select account:")
        for idx, acc in enumerate(accounts, start=1):
            print(f"{idx}. {acc.account_number} ({acc.type.value}, Balance: {acc.balance})")
        choice = input("Enter number: ")
        try:
            idx = int(choice) - 1
            return accounts[idx]
        except (IndexError, ValueError):
            print("Invalid selection.")
            return None

def check_balance(user):
    acc = select_account(user)
    if acc:
        print(f"Account {acc.account_number} balance: {acc.balance}")

def deposit(user):
    acc = select_account(user)
    if acc:
        amount_input = input("Enter amount to deposit: ")
        try:
            amount = Decimal(amount_input)
        except:
            print("Invalid amount.")
            return
        with Session() as session:
            acc = session.query(Account).filter_by(id=acc.id).first()
            acc.balance += amount
            transaction = Transaction(
                id=gen_uuid(),
                account_id=acc.id,
                amount=amount,
                type=TransactionType.DEPOSIT,
                reference="deposit"
            )
            session.add(transaction)
            session.commit()
            print(f"Deposited {amount}. New balance: {acc.balance}")

def withdraw(user):
    acc = select_account(user)
    if acc:
        amount_input = input("Enter amount to withdraw: ")
        try:
            amount = Decimal(amount_input)
        except:
            print("Invalid amount.")
            return
        if acc.balance < amount:
            print("Insufficient funds.")
            return
        with Session() as session:
            acc = session.query(Account).filter_by(id=acc.id).first()
            acc.balance -= amount
            transaction = Transaction(
                id=gen_uuid(),
                account_id=acc.id,
                amount=amount,
                type=TransactionType.WITHDRAWAL,
                reference="withdraw"
            )
            session.add(transaction)
            session.commit()
            print(f"Withdrew {amount}. New balance: {acc.balance}")

def transfer(user):
    from_acc = select_account(user)
    if not from_acc:
        return
    to_acc_number = input("Enter recipient account number: ")
    amount_input = input("Enter amount to transfer: ")
    try:
        amount = Decimal(amount_input)
    except:
        print("Invalid amount.")
        return

    with Session() as session:
        to_acc = session.query(Account).filter_by(account_number=to_acc_number).first()
        if not to_acc:
            print("Recipient account not found.")
            return
        if from_acc.balance < amount:
            print("Insufficient funds.")
            return

        # Update balances
        from_acc_db = session.query(Account).filter_by(id=from_acc.id).first()
        to_acc_db = session.query(Account).filter_by(id=to_acc.id).first()
        from_acc_db.balance -= amount
        to_acc_db.balance += amount

        # Transactions
        t1 = Transaction(
            id=gen_uuid(),
            account_id=from_acc_db.id,
            amount=amount,
            type=TransactionType.TRANSFER,
            reference=f"transfer to {to_acc_number}"
        )
        t2 = Transaction(
            id=gen_uuid(),
            account_id=to_acc_db.id,
            amount=amount,
            type=TransactionType.DEPOSIT,
            reference=f"transfer from {from_acc.account_number}"
        )
        session.add_all([t1, t2])
        session.commit()
        print(f"Transferred {amount} from {from_acc.account_number} to {to_acc_number}")

def transaction_history(user):
    acc = select_account(user)
    if acc:
        with Session() as session:
            transactions = session.query(Transaction).filter_by(account_id=acc.id).order_by(Transaction.created_at.desc()).all()
            if not transactions:
                print("No transactions found.")
                return
            print(f"Transaction history for {acc.account_number}:")
            for t in transactions:
                print(f"{t.created_at} | {t.type.value} | {t.amount} | {t.reference}")

if __name__ == "__main__":
    main_menu()
