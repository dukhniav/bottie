from bottie.persistance.base import ModelBase
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, relationship
from enum import Enum as PyEnum

from bottie.configuration.configuration import config
from bottie.constants import DEFAULT_ACCOUNT_NAME, DEFAULT_PORTFOLIO_NAME

engine = create_engine(config.get_db_url(), echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class TransactionType(PyEnum):
    PENDING = "pending"
    PROCESSED = "processed"


class Portfolio(ModelBase):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    accounts = relationship("Account", back_populates="portfolio")

    def __repr__(self):
        return f"Portfolio(id={self.id}, name='{self.name}')"


class Account(ModelBase):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    portfolio = relationship("Portfolio", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    exchange = Column(String, default="paper")
    available_funds = Column(Float, default=0.0)
    pending_funds = Column(Float, default=0.0)

    @property
    def total_funds(self):
        return self.available_funds + self.pending_funds

    def __repr__(self):
        return f"Account(id={self.id}, name='{self.name}', available_funds={self.available_funds}, pending_funds={self.pending_funds})"


class Transaction(ModelBase):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    type = Column(Enum(TransactionType), default=TransactionType.PENDING)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id={self.id}, symbol='{self.symbol}', quantity={self.quantity}, price={self.price}, type='{self.type}')"

    def process_transaction(self):
        total_cost = self.quantity * self.price
        self.account.available_funds -= total_cost
        self.type = TransactionType.PROCESSED
        session.commit()


ModelBase.metadata.create_all(engine)
