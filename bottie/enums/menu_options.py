from enum import Enum


class MenuOptions(Enum):
    """
    Bot menu options
    """

    START = 'start worker'
    STOP = 'stop worker'

    ACCOUNT_MANAGE = 'manage account'
    ACCOUNT_BALANCE = 'get account balance'
    ACCOUNT_AVAILABLE = 'get available funds'

    CONFIG_MANAGE = 'manage config'
    CONFIG_RELOAD = 'reload config'
    CONFIG_ADD_TICKER = 'add ticker'
    CONFIG_VIEW_TICKERS = 'view tickers'
    CONFIG_REMOVE_TICKER = 'remove ticker'

    MANUAL = 'manual'
    MANUAL_QUOTE = 'get quote'
    MANUAL_TRADE = 'manual trade'
    MANUAL_PENDING = 'check pending'
    MANUAL_GET_TRADES = 'get 10 last trades'

    QUIT_BOTTIE = 'quit bottie'
