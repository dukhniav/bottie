from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging

from bottie.configuration.configuration import config
from bottie.constants import DEFAULT_ACCOUNT_NAME, DEFAULT_PORTFOLIO_NAME
from bottie.persistance.models import Portfolio, Account

logger = logging.getLogger(__name__)


def initialize_models():
    logger.info("Initialize persistance models...")

    engine = create_engine(config.get_db_url(), echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    Portfolio.metadata.create_all(engine)
    Account.metadata.create_all(engine)

    # Check if a default portfolio exists
    default_portfolio = (
        session.query(Portfolio).filter_by(name=DEFAULT_PORTFOLIO_NAME).first()
    )
    if default_portfolio is None:
        # Create a default portfolio and account
        default_portfolio = Portfolio(name=DEFAULT_PORTFOLIO_NAME)
        default_account = Account(
            name=DEFAULT_ACCOUNT_NAME,
            portfolio=default_portfolio,
            available_funds=config.get_starting_funds(),
        )

        session.add(default_portfolio)
        session.add(default_account)
        session.commit()

    session.close()
