import json

from os import system, name, path

from asset_manager import AssetManager
from trx_manager import TransactionManager
from portfolio_manager import PortfolioManager

from enums import OrderSide

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
        clear()

        print("╔═════════════════════════════════╗")
        print("║        MENU                     ║")
        print("╠═════════════════════════════════╣")
        print("║ Please select an option:        ║")
        print("║   1. View balance               ║")
        print("║   2. View assets                ║")
        print("║   3. Get quote                  ║")
        print("║   4. Portfolio performance      ║")
        print("║   5. Stock performance          ║")
        print("║   6. Submit order               ║")
        print("║   9. Restart                    ║")
        print("║   0. Quit                       ║")
        print("╚═════════════════════════════════╝")

        try:
            option = int(input('Your option: '))
        except ValueError:
            option = 999

        if option == 1:
            print(f'\n    Balance: {portfolio_manager.get_balance()}\n')
        elif option == 2:
            print(f'\n    Assets: {asset_manager.get_assets()}\n')
        elif option == 3:
            # get quote
            assets = []
            asset_dict = asset_manager.load_assets()
            if asset_dict is not None:
                asset_dict = asset_dict.items()

                print('\n    Enter stock ticker, or choose from below: ')
                for key, value in asset_dict:
                    temp = [key, value['quantity']]
                    assets.append(temp)

                for i, ticker in enumerate(assets, 1):
                    print(f" {i}. {ticker[0]} ({ticker[1]})")

                selection = input("\n> ")
                try:
                    selection = int(selection) - 1
                    ticker = assets[selection][0]
                except:
                    ticker = selection.upper()
            else:
                ticker = input('\n    Enter stock ticker: ').upper()

            price = finnhub_api.get_quote(ticker)['price']

            f_price = f'{price:,.2f}'
            print(f'\n    Current "{ticker}" market price: ${f_price}.')
        elif option == 4:
            print(transaction_manager.get_stock_performance())
        elif option == 5:
            print('\n    Not implemented.')
        elif option == 6:
            # Submit order

            print(
                "\n    Order details:\n       1. Buying\n       2. Selling\n       3. Cancel\n")

            try:
                action = int(input('Enter action: '))
            except ValueError:
                action = 999
            if action == 3:
                # 3. Cancel
                continue
            elif action in [1, 2]:
                if action == 1:
                    # Buy

                    ticker = input('\n    Enter stock ticker: ').upper()
                else:
                    # Sell

                    print('\n    Available stocks to sell:\n')

                    try:
                        ticker = get_ticker(asset_manager)
                    except IndexError:
                        print('\n    Sorry, stock not found...')

                # price = float(input('Enter price: '))
                qty = int(input('    Enter quantity (whole shares only): '))
                order_side = OrderSide.BUY if action == 1 else OrderSide.SELL
                transaction_manager.record_transaction(
                    ticker, qty, order_side)
            else:
                print('Invalid option, try again...')
        elif option == 9:
            run = False
            restart = True
        elif option == 0:
            print('\n    Thank you for using this "awesome" program.\nExiting...\n')
            run = False
            break
        else:
            print('Invalid option, try again...')

        if restart:
            input('\nPress any key to restart...')
        else:
            input('\nPress any key to continue...')

    # Restart
    if restart:
        main()


def get_ticker(assets: AssetManager):
    assets = []
    assets_dict = assets.load_assets().items()
    for key, value in assets_dict:
        temp = [key, value['quantity']]
        assets.append(temp)

    for i, ticker in enumerate(assets, 1):
        print(f" {i}. {ticker[0]} ({ticker[1]})")

    sell_selection = int(input("\n> ")) - 1

    return assets[sell_selection][0]


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


if __name__ == '__main__':
    main()
