from __future__ import annotations
import enum
import uuid
from decimal import Decimal
from datetime import datetime
from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Column,
    DateTime,
    ForeignKey,
    Enum,
    Numeric,
    Boolean,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column, sessionmaker

# ===========================================
# BASE
# ===========================================
Base = declarative_base()

# ===========================================
# UTILS
# ===========================================
def gen_uuid() -> str:
    return str(uuid.uuid4())

def now_utc() -> datetime:
    return datetime.utcnow()

# ===========================================
# ENUMS
# ===========================================
class AccountType(enum.Enum):
    SAVINGS = "savings"
    CHECKING = "checking"
    CREDIT = "credit"

class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    FEE = "fee"

# ===========================================
# MODELS
# ===========================================
class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())

    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")
    cards = relationship("Card", back_populates="owner", cascade="all, delete-orphan")
    beneficiaries = relationship("Beneficiary", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email} id={self.id}>"

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    owner_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    account_number: Mapped[str] = mapped_column(String(34), unique=True, nullable=False)
    type: Mapped[AccountType] = mapped_column(Enum(AccountType), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(18,2), default=Decimal("0.00"))
    currency: Mapped[str] = mapped_column(String(8), default="KES")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())

    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

    def deposit(self, amount: Decimal):
        self.balance += amount

    def withdraw(self, amount: Decimal):
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def __repr__(self):
        return f"<Account {self.account_number} balance={self.balance}>"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    account_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18,2), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())

    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.id} account={self.account_id} {self.type} {self.amount}>"

class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    owner_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_number: Mapped[str] = mapped_column(String(34), nullable=False)
    bank_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())

    owner = relationship("User", back_populates="beneficiaries")

    def __repr__(self):
        return f"<Beneficiary {self.name} {self.account_number}>"

class Card(Base):
    __tablename__ = "cards"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    owner_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    card_mask: Mapped[str] = mapped_column(String(19), nullable=False)
    last4: Mapped[str] = mapped_column(String(4), nullable=False)
    expiry_month: Mapped[int] = mapped_column(Integer, nullable=False)
    expiry_year: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())

    owner = relationship("User", back_populates="cards")

    def __repr__(self):
        return f"<Card ****{self.last4} owner={self.owner_id}>"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())

    def __repr__(self):
        return f"<Audit {self.action} {self.entity} {self.entity_id}>"

# ===========================================
# DATABASE SETUP
# ===========================================
engine = create_engine("sqlite+pysqlite:///./bank.db", echo=True, future=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Create tables if they don't exist
Base.metadata.create_all(engine)
