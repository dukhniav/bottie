class Menu:
    def __init__(self):
        self.menu_options = {}

    def add_option(self, option, label, action):
        self.menu_options[option] = (label, action)

    def display_menu(self):
        print("Menu:")
        for option, (label, _) in self.menu_options.items():
            print(f"{option}. {label}")

        try:
            option = int(input("Enter option number: "))
            if option in self.menu_options:
                _, selected_action = self.menu_options[option]
                if selected_action:
                    selected_action()
                else:
                    print("Invalid option. Please try again.")
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid option. Please try again.")

    def setup_main_menu(self):
        # Initialize the main menu options
        self.add_option(1, "Start Bot", self.start_bot)
        self.add_option(2, "Stop Bot", self.stop_bot)
        self.add_option(3, "View Config", self.view_config)

    def setup_ticker_menu(self):
        # Initialize the ticker management submenu options
        self.add_option(1, "Add Ticker", self.add_ticker)
        self.add_option(2, "Remove Ticker", self.remove_ticker)
        self.add_option(3, "Back to Main Menu", None)

    def setup_account_menu(self):
        # Initialize the account management submenu options
        self.add_option(1, "Create Account", self.create_account)
        self.add_option(2, "Get Account Worth", self.get_account_worth)
        self.add_option(3, "Get Portfolio", self.get_portfolio)
        self.add_option(4, "Back to Main Menu", None)
