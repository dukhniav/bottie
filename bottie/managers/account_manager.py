from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bottie.persistance.models import Account

from bottie.configuration.configuration import config
from bottie.constants import DEFAULT_ACCOUNT_NAME

engine = create_engine(config.get_db_url(), echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class AccountManager:
    def get_account_by_name(self, account_name=DEFAULT_ACCOUNT_NAME):
        """
        Retrieve an account by its name.
        """
        account = session.query(Account).filter_by(name=account_name).first()
        return account

    def get_account_count():
        engine = create_engine(config.get_db_url(), echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        account_count = session.query(Account).count()

        session.close()

        return account_count

    def get_accounts(self):
        """
        Retrieve all accounts.
        """
        accounts = session.query(Account).all()
        return accounts

    def get_account_available_funds(self, account_name=DEFAULT_ACCOUNT_NAME):
        """
        Return account available balance
        """
        account = self.get_account_by_name(account_name)
        if account:
            return account.available_funds
        return None

    def get_total_funds(self, account_name=DEFAULT_ACCOUNT_NAME):
        """
        Calculate the total funds (available + pending) for an account.
        """
        account = self.get_account_by_name(account_name)
        if account:
            return account.total_funds
        return None

    def update_account_funds(
        self,
        account_name=DEFAULT_ACCOUNT_NAME,
        available_funds=None,
        pending_funds=None,
    ):
        """
        Update the available and/or pending funds of an account.
        """
        account = self.get_account_by_name(account_name)
        if account:
            if available_funds is not None:
                account.available_funds = available_funds
            if pending_funds is not None:
                account.pending_funds = pending_funds
            session.commit()
            return True
        return False

    def delete_account(self, account_name):
        """
        Delete an account by its name.
        """
        account = self.get_account_by_name(account_name)
        if account:
            session.delete(account)
            session.commit()
            return True
        return False
