from os import system, name

from asset_manager import AssetManager
from trx_manager import TransactionManager
from portfolio_manager import PortfolioManager


def main():
    asset_manager = AssetManager()
    portfolio_manager = PortfolioManager()
    transaction_manager = TransactionManager(
        asset_mng=asset_manager, prt_mng=portfolio_manager)

    # print(portfolio_manager.get_balance())
    # # Buy 10 shares of AAPL
    # transaction_manager.record_transaction('AAPL', 'Buy', 10, 130.50)

    # # Sell 5 shares of AAPL
    # # asset_manager.sell_asset('AAPL', 5)
    # transaction_manager.record_transaction('AAPL', 'Sell', 5, 135.20)
    # transaction_manager.record_transaction('AAPL', 'Sell', 100, 140)
    # # portfolio_manager.update_balance(5 * 135.20)
    # transaction_manager.record_transaction('MSFT', 'Buy', 10, 200)

    # print(portfolio_manager.get_balance())
    # print(asset_manager.get_assets())

    # print(portfolio_manager.get_balance())
    run = True

    while run:
        clear()

        print('-------- MENU --------')
        print('Please select an option:')
        print('    1. View balance')
        print('    2. View assets')
        print('    3. Submit an order')
        print('    4. Quit')

        try:
            option = int(input('Your option: '))
        except ValueError:
            option = 999

        if option == 1:
            print(f'\n    {portfolio_manager.get_balance()}')
        elif option == 2:
            print(f'\n    {asset_manager.get_assets()}')
        elif option == 3:
            print(
                'Order details: \n        1. Buying\n        2. Selling\n        3. Cancel')
            try:
                action = int(input('Enter action: '))
            except ValueError:
                action = 999

            if action == 3:
                continue
            elif action in [1, 2]:
                if action == 1:
                    ticker = input('Enter stock ticker: ').upper()
                else:
                    print('    Avaiable stocks to sell:')

                    assets = []
                    assets_dict = asset_manager.load_assets().items()
                    for key, value in assets_dict:
                        temp = [key, value['quantity']]
                        assets.append(temp)

                    for i, ticker in enumerate(assets, 1):
                        print(' ' * 8 + str(i) + ' -> ' +
                              ticker[0] + ' (' + str(ticker[1]) + ')')
                    sell_selection = int(input("    > ")) - 1
                    try:
                        ticker = assets[sell_selection][0]
                    except IndexError:
                        print('    Sorry, stock not found...')
                price = float(input('Enter price: '))
                qty = int(input('Enter quantity (whole shares only): '))
                transaction_manager.record_transaction(
                    ticker, 'Buy' if action == 1 else 'Sell', qty, price)
            else:
                print('Invalid option, try again...')
        elif option == 4:
            print('\nThank you for using this "awesome" program. \n\nExiting...\n')
            run = False
            break
        else:
            print('Invalid option, try again...')
        input('\nPress any key to continue...')


# define our clear function


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


if __name__ == '__main__':
    main()
