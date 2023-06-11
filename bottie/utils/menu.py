import os
import threading
import getch

from typing import Dict

from bottie.enums.menu_options import MenuOptions

from bottie.bottie import bottie


def start_worker():
    if bottie.start_worker():
        return "Worker started."
    else:
        return "Unable to start worker."


def stop_worker():
    if bottie.stop_worker():
        return "Worker stopped."
    else:
        return "Unable to stop worker."


def get_account_balance():
    return MenuOptions.ACCOUNT_BALANCE


def get_available_funds():
    avail_funds = bottie.show_available_funds()
    msg = f'Available funds: ${avail_funds}'
    return format_result(msg)


def reload_config():
    return MenuOptions.CONFIG_RELOAD


def view_tickers():
    return MenuOptions.CONFIG_VIEW_TICKERS


def add_ticker():
    return MenuOptions.CONFIG_ADD_TICKER


def remove_ticker():
    return MenuOptions.CONFIG_REMOVE_TICKER


def get_quote():
    quote: Dict = bottie.get_quote()
    msg = f"Price for {quote.get('ticker')}: {quote.get('quote')}"
    return format_result(msg)


def submit_manual_trade():
    return MenuOptions.MANUAL_TRADE


def view_pending_trades():
    return MenuOptions.MANUAL_PENDING


def get_last_trades():
    return MenuOptions.MANUAL_GET_TRADES


menu = {
    1: (MenuOptions.START.value, start_worker),
    2: (MenuOptions.STOP.value, stop_worker),
    3: (MenuOptions.ACCOUNT_MANAGE.value, {
        1: (MenuOptions.ACCOUNT_BALANCE.value, get_account_balance),
        2: (MenuOptions.ACCOUNT_AVAILABLE.value, get_available_funds)
    }),
    4: (MenuOptions.CONFIG_MANAGE.value, {
        1: (MenuOptions.CONFIG_RELOAD.value, reload_config),
        2: (MenuOptions.CONFIG_VIEW_TICKERS.value, view_tickers),
        3: (MenuOptions.CONFIG_ADD_TICKER.value, add_ticker),
        4: (MenuOptions.CONFIG_REMOVE_TICKER.value, remove_ticker)
    }),
    5: (MenuOptions.MANUAL.value, {
        1: (MenuOptions.MANUAL_QUOTE.value, get_quote),
        2: (MenuOptions.MANUAL_TRADE.value, submit_manual_trade),
        3: (MenuOptions.MANUAL_PENDING.value, view_pending_trades),
        4: (MenuOptions.MANUAL_GET_TRADES.value, get_last_trades)
    })}


def display_menu(menu_options, indent=0, is_outermost_menu=False):
    for option in menu_options:
        if isinstance(menu_options[option], tuple):  # Regular option
            label, _ = menu_options[option]
            print('\t' * indent + f'{option}. {label}')
        else:  # Submenu
            label, _ = menu_options[option]
            print('\t' * indent + f'{option}. {label}')
    if is_outermost_menu:
        print('\t' * indent + '0. quit')
    else:
        print('\t' * indent + '0. back to Main Menu')


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def press_any_key():
    print("\nPress any key to continue...")
    getch.getch()


def execute_action(action):
    if callable(action):
        return action()
    else:
        return None


def format_result(result: str):
    offset = 5  # Number of characters to offset

    # Add offset spaces
    result = " " * offset + result

    formatted_result = f"\n{'-' * (len(result) + offset)}\
        \n{result}\
        \n{'-' * (len(result) + offset)}"

    return formatted_result


def handle_menu_action(result):
    clear_screen()
    print("Action Result:")
    if result is not None:
        print(result)
    else:
        print("No action result.")
    press_any_key()
    clear_screen()


def run_submenu(callback, submenu):
    while True:
        clear_screen()
        print("Submenu:")
        display_menu(submenu)
        choice = input("Enter your choice: ")

        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                break  # Go back to the main menu
            elif choice in submenu:
                _, action = submenu[choice]
                result = execute_action(action)
                handle_menu_action(result)
            else:
                print("Invalid choice. Please try again.")
                press_any_key()
        else:
            print("Invalid choice. Please enter a number.")
            press_any_key()

        if callback:
            callback(result)


def main_menu(callback=None):
    while True:
        clear_screen()
        print("Main Menu:")
        display_menu(menu, is_outermost_menu=True)
        choice = input("Enter your choice: ")

        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                break  # Exit the program
            elif choice in menu:
                _, action = menu[choice]
                if isinstance(action, dict):  # Submenu
                    run_submenu(callback, action)
                else:  # Regular option
                    result = execute_action(action)
                    handle_menu_action(result)
                    if callback:
                        callback(result)
            else:
                print("Invalid choice. Please try again.")
                press_any_key()
        else:
            print("Invalid choice. Please enter a number.")
            press_any_key()


def run_menu_in_thread(callback=None, menu_options=None):
    thread = threading.Thread(target=main_menu, args=(callback,))
    if menu_options:
        thread = threading.Thread(
            target=run_submenu, args=(callback, menu_options))
    thread.start()
