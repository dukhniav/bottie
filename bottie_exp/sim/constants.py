

# Menu handling
MENU_INVALID_OPTION = '\n    Invalid option, try again...'
MENU_RESTART_OPTION = '\n    Press any key to restart...'
MENU_CONTINUE_ANY_KEY = 'Press ENTER to continue...'
MENU_EXIT_MSG = '\n    Thank you for using this "awesome" program.\nExiting...\n'
MENU_ASSET_QUOTE_CHOOSE = '\n    Enter stock ticker, or choose from below: '

# Balance error handling
BALANCE_LOW_ERR = 'Balance too low to cover transaction.'
BALANCE_UPDATE_ERR = 'Error updating balance file.'
BALANCE_GET_ERR = 'Unable to get balance.'
BALANCE_FILE_ERR = 'Cannot find balance file.'

# Asset error handling
ASSET_UPDATE_ERR = 'Error updating asset file.'
ASSET_GET_ERR = 'Unable to get assets.'
ASSET_FILE_ERR = 'Cannot find asset file.'
ASSET_NO_ASSETS = 'No assets to display.'

# Transaction error handling
TRX_UPDATE_ERR = 'Error updating transactions file.'
TRX_GET_ERR = 'Unable to get transactions.'
TRX_FILE_ERR = 'Cannot find transactions file.'
TRX_CREATE_ERR = 'Something went wrong with creating the transaction...'
TRX_SAVE_ERR = 'Something went wrong with saving transactions...'
TRX_ASSET_UPDATE_ERR = 'Somethign went wrong with updating assets...'
TRX_MSG_CREATE_ERR = 'Something went wrong with generating order message...'
INVALID_TICKER_ERR = 'Invalid ticker'
TRX_NEXT_ID = 'Error generating next transaction id.'
TRX_TRX_BY_TICKER = 'Unable to retrieve transactions for ticker.'


def display_err(error_msg) -> bool:
    print(f'\n    Error: {error_msg}')
    return False


def format_currency(currency_number: float) -> str:
    formatted_number = f'{currency_number:,.2f}'
    return formatted_number


def format_percent(percent: float, _len: int) -> str:
    formatted_percent = round(percent, _len)
    return str(formatted_percent)
