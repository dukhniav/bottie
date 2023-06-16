
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.collections import InstrumentedList


from typing import List

from bottie.persistance.models import Transaction, Account, TransactionType

from bottie.configuration.configuration import config
from bottie.constants import DEFAULT_ACCOUNT_NAME


engine = create_engine(config.get_db_url(), echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class TransactionManager:
    def create_transaction(self, symbol, quantity, price, account_name=DEFAULT_ACCOUNT_NAME):
        """
        Create a new transaction for the specified account and set it as "pending".
        """
        account = session.query(Account).filter_by(name=account_name).first()
        if account:
            transaction = Transaction(
                symbol=symbol, quantity=quantity, price=price, type=TransactionType.PENDING)
            account.transactions.append(transaction)
            session.commit()
            return transaction
        return None

    def get_transactions(self, account_name=DEFAULT_ACCOUNT_NAME) -> InstrumentedList:
        """
        Retrieve all transactions for the specified account.
        """
        account = session.query(Account).filter_by(name=account_name).first()
        if account:
            return account.transactions
        return []

    def process_transactions(self, account_name=DEFAULT_ACCOUNT_NAME) -> bool:
        """
        Process all pending transactions for the specified account.
        Deducts the transaction cost from the account's available funds and marks transactions as "processed".
        """
        account = session.query(Account).filter_by(name=account_name).first()
        if account:
            transactions: InstrumentedList = account.transactions
            for transaction in transactions:
                if transaction.type == TransactionType.PENDING:
                    transaction.process_transaction()
            session.commit()
            return True
        return False

    def delete_transaction(self, transaction_id):
        """
        Delete a transaction by its ID.
        """
        transaction = session.query(Transaction).filter_by(
            id=transaction_id).first()
        if transaction:
            session.delete(transaction)
            session.commit()
            return True
        return False
