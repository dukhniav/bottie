import os
import threading
import getch

from bottie.enums.menu_options import MenuOptions


def get_account_value():
    return "Getting account value..."


# Add other menu functions here
def callback_value(value):
    return value


def exit_program():
    return "Exiting program..."
    quit()


menu = {
    1: (MenuOptions.START.value, callback_value(MenuOptions.START)),
    2: (MenuOptions.STOP.value, callback_value(MenuOptions.STOP)),
    3: (MenuOptions.ACCOUNT_MANAGE.value, {
        1: (MenuOptions.ACCOUNT_BALANCE.value, callback_value(MenuOptions.ACCOUNT_BALANCE)),
        2: (MenuOptions.ACCOUNT_AVAILABLE.value, callback_value(MenuOptions.ACCOUNT_AVAILABLE))
    }),
    4: (MenuOptions.CONFIG_MANAGE.value, {
        1: (MenuOptions.CONFIG_RELOAD.value, callback_value(MenuOptions.CONFIG_RELOAD)),
        2: (MenuOptions.CONFIG_VIEW_TICKERS.value, callback_value(MenuOptions.CONFIG_VIEW_TICKERS)),
        3: (MenuOptions.CONFIG_ADD_TICKER.value, callback_value(MenuOptions.CONFIG_ADD_TICKER)),
        4: (MenuOptions.CONFIG_REMOVE_TICKER.value, callback_value(MenuOptions.CONFIG_REMOVE_TICKER))
    }),
    5: (MenuOptions.MANUAL.value, {
        1: (MenuOptions.MANUAL_QUOTE.value, callback_value(MenuOptions.MANUAL_QUOTE)),
        2: (MenuOptions.MANUAL_TRADE.value, callback_value(MenuOptions.MANUAL_TRADE)),
        3: (MenuOptions.MANUAL_PENDING.value, callback_value(MenuOptions.MANUAL_PENDING)),
        4: (MenuOptions.MANUAL_GET_TRADES.value, callback_value(MenuOptions.MANUAL_GET_TRADES))
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


def handle_menu_action(result):
    clear_screen()
    print("Action Result:")
    print(result)
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
