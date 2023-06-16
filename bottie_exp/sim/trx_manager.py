import json
import os
from datetime import datetime

from asset_manager import AssetManager
from portfolio_manager import PortfolioManager

TRANSACTIONS_FILE = 'data/transactions.json'


class TransactionManager:
    def __init__(self, asset_mng: AssetManager, prt_mng: PortfolioManager):
        self.assets = asset_mng
        self.portfolio = prt_mng
        self.type = None
        self.transactions = self.load_transactions()

    @staticmethod
    def get_transactions():
        trx = TransactionManager.load_transactions()
        print(f'Transactions: {trx}')

    @staticmethod
    def load_transactions():
        if os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE) as file:
                return json.load(file)
        return []

    def save_transactions(self):
        with open(TRANSACTIONS_FILE, 'w') as file:
            json.dump(self.transactions, file, indent=4)

    def record_transaction(self, symbol, action, quantity, price):
        msg = ''
        transaction = {
            'symbol': symbol,
            'action': action,
            'quantity': quantity,
            'price': price,
            'timestamp': datetime.now().isoformat()
        }

        self.transactions.append(transaction)
        self.save_transactions()

        total = quantity * price
        formatted_total = f'{total:,.2f}'
        formatted_price = f'{price:,.2f}'
        if action == 'Buy':
            msg = f"Buying {quantity} of {symbol} @ ${formatted_price} (${formatted_total})."

            self.assets.add_asset(symbol, quantity)
            self.portfolio.update_balance(-1 * total)
        elif action == 'Sell':
            msg = f"Selling {quantity} of {symbol} @ ${formatted_price} (${formatted_total})."

            self.assets.remove_asset(symbol, quantity)
            self.portfolio.update_balance(total)

        print(msg)
