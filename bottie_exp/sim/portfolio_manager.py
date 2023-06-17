import json
import os

BALANCE_FILE = 'data/balance.json'


class PortfolioManager:
    def __init__(self):
        self.balance = self._load_balance()

    @staticmethod
    def _load_balance():
        if os.path.exists(BALANCE_FILE):
            with open(BALANCE_FILE) as file:
                balance = json.load(file)
            return balance['balance']
        return 0

    @staticmethod
    def get_balance():
        balance = PortfolioManager._load_balance()

        formatted_balance = f'{balance:,.2f}'

        msg = f"Current balance: ${formatted_balance}."
        return msg

    def save_balance(self, new_balance):
        balance = {
            "balance": new_balance
        }
        with open(BALANCE_FILE, 'w') as file:
            json.dump(balance, file)

    def update_balance(self, amount) -> bool:
        try:
            bal = self.balance
            self.balance = bal + amount
            self.save_balance(self.balance)
            return True
        except:
            return False
