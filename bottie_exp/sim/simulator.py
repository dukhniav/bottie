import json
import os
import platform
from typing import Dict, List, Any

from asset_manager import AssetManager
from trx_manager import TransactionManager
from portfolio_manager import PortfolioManager
from enums import OrderSide
from constants import display_err, format_percent, format_currency, ASSET_NO_ASSETS, MENU_CONTINUE_ANY_KEY, MENU_INVALID_OPTION, MENU_RESTART_OPTION, MENU_EXIT_MSG, MENU_ASSET_QUOTE_CHOOSE
from finnhub_api import finnhub_api

EXCHANGE = 'finnhub'


def main():
    asset_manager = AssetManager()
    portfolio_manager = PortfolioManager()
    transaction_manager = TransactionManager(
        asset_mng=asset_manager, prt_mng=portfolio_manager)
    run = True
    restart = False

    while run:
        display_menu()
        try:
            option = int(input('Your option: '))
        except ValueError:
            option = 999

        if option == 1:  # get current balance
            menu_balance(portfolio_manager)
        elif option == 2:  # view assets
            menu_assets(asset_manager)
        elif option == 3:
            menu_quote(asset_manager)
        elif option == 4:
            menu_performance(transaction_manager)
        elif option == 5:
            menu_order(asset_manager, transaction_manager)
        elif option == 9:
            run = False
            restart = True
        elif option == 0:
            display_err(MENU_EXIT_MSG)
            run = False
            break
        else:
            display_err(MENU_INVALID_OPTION)

        if restart:
            input(MENU_RESTART_OPTION)
        else:
            input(MENU_CONTINUE_ANY_KEY)

    # Restart
    if restart:
        main()


def display_results(msg: str):
    print(msg)


def menu_balance(portfolio: PortfolioManager):
    balance = format_currency(portfolio.get_balance())
    print(f'\n    Balance: ${balance}\n')


def menu_assets(am: AssetManager):
    assets: Dict = am.get_assets()
    msg = '\n'
    if assets:
        msg += ' ' * 4 + 'Currently owned assets:'
        for asset in assets:
            msg += '\n' + ' ' * 8 + asset
            msg += ' - ' + str(assets[asset]['quantity'])
    else:
        msg += ' ' * 4 + 'No owned assets.'
    msg += '\n'
    print(msg)


def menu_quote(assets: AssetManager):
    assets: List = []
    asset_dict = AssetManager.get_assets()

    if asset_dict:
        asset_dict = asset_dict.items()

        print(MENU_ASSET_QUOTE_CHOOSE)
        for key, value in asset_dict:
            temp = [key, value['quantity']]
            assets.append(temp)

        asset_msg = ''
        for i, ticker in enumerate(assets, 1):
            asset_msg += ' ' * 8 + str(i) + '. ' + \
                ticker[0] + '(' + str(ticker[1]) + ')\n'
        print(asset_msg)

        selection = input("    > ")
        try:
            selection = int(selection) - 1
            ticker = assets[selection][0]
        except:
            ticker = selection.upper()
    else:
        ticker = input('\n    Enter stock ticker: ').upper()

    price = finnhub_api.get_quote(ticker)['price']
    f_price = format_currency(price)

    msg = '\n' + ' ' * 4 + f'Current "{ticker}" market price: ${f_price}.\n'
    print(msg)


def menu_performance(transactions: TransactionManager):
    performance = transactions.get_performance()
    stock_perf = performance['stocks']
    bt = performance['total_buy']
    ct = performance['total_current']
    pc = bt/ct

    direction = get_direction(bt, ct)
    msg = f'\n    '
    msg += f'Portfolio {direction}. ' if bt == ct else f"Portfolio {direction} by {format_percent(pc, 2)}%. "
    msg += f'Current worth: ${format_currency(ct)}'

    if direction == 'even':
        msg += '.\n\n'
    else:
        msg += f' ({direction} by ${format_currency(ct - bt)}).\n\n'

    s_msg = '\n'
    s_dir = ''

    if stock_perf:
        for k, v in stock_perf.items():
            bt = v['buy_total']
            ct = v['cur_total']
            pc = bt/ct if ct > 0 else 0
            direction = get_direction(bt, ct)

            s_msg += f'    {k} '
            s_dir = f'{direction}'

            if direction != 'even':
                s_dir += f' {format_percent(pc)}%. '
            else:
                s_dir += '. '

            s_msg += s_dir
            s_msg += f'Current worth: ${format_currency(ct)}. \n'

        tmp_msg = msg
        msg = s_msg
        msg += tmp_msg

    print(msg)


def get_direction(original, current) -> str:
    direction = 'up' if current > original else 'down' if current < original else 'even'
    return direction


def menu_order(am: AssetManager, tm: TransactionManager):
    # Submit order
    print("\n    Order details:\n       1. Buying\n       2. Selling\n       3. Cancel\n")

    try:
        action = int(input('Enter action: '))
    except ValueError:
        action = 999

    if action == 3:
        # 3. Cancel
        pass
    elif action in [1, 2]:
        if action == 1:
            # Buy
            ticker = input('\n    Enter stock ticker: ').upper()
        else:
            assets: List = []
            asset_dict = AssetManager.get_assets()

            if asset_dict:
                asset_dict = asset_dict.items()

                print(MENU_ASSET_QUOTE_CHOOSE)
                for key, value in asset_dict:
                    temp = [key, value['quantity']]
                    assets.append(temp)

                asset_msg = ''
                for i, ticker in enumerate(assets, 1):
                    asset_msg += ' ' * 8 + \
                        str(i) + '. ' + ticker[0] + \
                        '(' + str(ticker[1]) + ')\n'
                print(asset_msg)

                selection = input("    > ")
                try:
                    selection = int(selection) - 1
                    ticker = assets[selection][0]
                except:
                    ticker = selection.upper()
            else:
                print(f'\n    {ASSET_NO_ASSETS}\n')

        qty = int(input('    Enter quantity (whole shares only): '))
        order_side = OrderSide.BUY if action == 1 else OrderSide.SELL
        tm.record_transaction(ticker, qty, order_side)
    else:
        display_err(MENU_INVALID_OPTION)


def display_menu():
    clear()

    print("╔═════════════════════════════════╗")
    print("║              MENU               ║")
    print("╠═════════════════════════════════╣")
    print("║ Please select an option:        ║")
    print("║   1. View balance               ║")
    print("║   2. View assets                ║")
    print("║   3. Get quote                  ║")
    print("║   4. Portfolio performance      ║")
    print("║   5. Submit order               ║")
    print("║   9. Restart                    ║")
    print("║   0. Quit                       ║")
    print("╚═════════════════════════════════╝")


def clear():
    # for windows
    if platform.system() == 'Windows':
        os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')


if __name__ == '__main__':
    main()
