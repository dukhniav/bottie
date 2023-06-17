import json
import os
from datetime import datetime
from typing import Dict

from asset_manager import AssetManager
from portfolio_manager import PortfolioManager

from enums import OrderSide, OrderType

from finnhub_api import finnhub_api

TRANSACTIONS_FILE = 'data/transactions.json'

TRX_CREATE_ERR = 'Something went wrong with creating the transaction...'
TRX_SAVE_ERR = 'Something went wrong with saving transactions...'
ASSET_UPDATE_ERR = 'Somethign went wrong with updating assets...'
MSG_CREATE_ERR = 'Something went wrong with generating order message...'
PRT_UPDATE_ERR = ' updating balance...'
INVALID_TICKER_ERR = ' Invalid ticker'


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
            try:
                with open(TRANSACTIONS_FILE) as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}

    def save_transactions(self):
        try:
            with open(TRANSACTIONS_FILE, 'w') as file:
                json.dump(self.transactions, file)
            file.close()
            return True
        except:
            return False

    def get_next_id(self) -> str:
        try:
            with open(TRANSACTIONS_FILE, 'r') as file:
                data = json.load(file)
            file.close()

            ids = [int(item) for item in data]
            print(ids)
            if ids:
                max_id = max(ids)
                next_id = max_id + 1
            else:
                next_id = 1
        except json.JSONDecodeError:
            next_id = str(1)

        return next_id

    def get_transactions_for_ticker(self, ticker):
        transactions = [
            transaction
            for transaction in self.transactions.values()
            if transaction.get('symbol') == ticker
        ]

        return transactions

    def get_stock_performance(self):
        assets = self.assets.assets
        transactions = self.transactions

        stock_performance = {}

        for transaction_id, transaction in transactions.items():
            symbol = transaction["symbol"]
            action = transaction["action"]
            quantity = transaction["quantity"]
            price = transaction["price"]
            timestamp = transaction["timestamp"]

            if symbol in assets:
                if action == "buy":
                    if quantity <= assets[symbol]["quantity"]:
                        assets[symbol]["quantity"] -= quantity
                        stock_performance[transaction_id] = {
                            "symbol": symbol,
                            "quantity": quantity,
                            "price": price,
                            "timestamp": timestamp
                        }
                    else:
                        remaining_quantity = assets[symbol]["quantity"]
                        assets[symbol]["quantity"] = 0
                        stock_performance[transaction_id] = {
                            "symbol": symbol,
                            "quantity": remaining_quantity,
                            "price": price,
                            "timestamp": timestamp
                        }
                elif action == "sell":
                    assets[symbol]["quantity"] += quantity
                    if symbol in stock_performance:
                        del stock_performance[symbol]

        for transaction_id, performance in stock_performance.items():
            symbol = performance["symbol"]
            latest_price = finnhub_api.get_quote(symbol)
            performance["latest_price"] = latest_price

        buy_total = 0
        cur_total = 0
        for x, y in stock_performance.items():
            symbol = y.get('symbol')
            price = y.get('price')
            qty = y.get('quantity')
            cur_price = y.get('latest_price')['price'] + 10
            delta = cur_price / price
            buy_total += price * qty
            cur_total += cur_price * qty

            # print(symbol, price, qty, cur_price, delta)
        direction = 'up' if cur_total > buy_total else 'down'
        msg = f'\n    Portfolio {direction} by {buy_total/cur_total}%. Current worth: ${cur_total} ({direction} by ${cur_total - buy_total})'
        return msg

    def record_transaction(self, symbol: str, quantity: int, action: OrderSide, _type: OrderType = OrderType.MARKET.value) -> bool:
        # Create transaction
        status = True
        symbol = symbol.upper()
        temp_trx = self.transactions

        try:
            price = finnhub_api.get_quote(symbol)['price']
        except:
            print(f'{INVALID_TICKER_ERR}: {symbol}')
            status = False

        msg = ''

        if status:
            try:
                next_id = self.get_next_id()

                transaction = {
                    'symbol': symbol,
                    'action': action.value,
                    'quantity': quantity,
                    'price': price,
                    'timestamp': datetime.now().isoformat()
                }

                temp_trx[next_id] = transaction
            except:
                print(TRX_CREATE_ERR)
                status = False

        if status:
            try:
                total = quantity * price
                formatted_total = f'{total:,.2f}'
                formatted_price = f'{price:,.2f}'

                # Generate message
                if action == OrderSide.BUY:
                    msg = f"Submitting BUY ({_type}) order of {quantity} of {symbol} @ ${formatted_price} (${formatted_total})."
                    total = -1 * total
                elif action == OrderSide.SELL:
                    msg = f"Selling {quantity} of {symbol} @ ${formatted_price} (${formatted_total})."

            except:
                print()

        # Save assets
        if status:
            status = self.assets.update_assets(action, symbol, quantity)
        else:
            err = MSG_CREATE_ERR

        # Update portfolio balance
        if status:
            status = self.portfolio.update_balance(total)
        else:
            err = ASSET_UPDATE_ERR

        if status:
            # Save transaction
            self.transactions = temp_trx
            status = self.save_transactions()
        else:
            err = PRT_UPDATE_ERR

        if status:
            print(msg)
            return True
        else:
            err = TRX_SAVE_ERR

        print(err)
        return False
