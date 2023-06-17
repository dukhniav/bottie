import json
import os
from datetime import datetime
from typing import Dict, AnyStr

from asset_manager import AssetManager
from portfolio_manager import PortfolioManager

from enums import OrderSide, OrderType

from finnhub_api import finnhub_api

from constants import format_percent, format_currency, display_err
from constants import TRX_UPDATE_ERR, TRX_FILE_ERR, TRX_GET_ERR, TRX_CREATE_ERR, TRX_MSG_CREATE_ERR, TRX_NEXT_ID, TRX_SAVE_ERR, TRX_TRX_BY_TICKER, INVALID_TICKER_ERR

TRANSACTIONS_FILE = 'data/transactions.json'


class TransactionManager:
    def __init__(self, asset_mng: AssetManager, prt_mng: PortfolioManager):
        self.assets = asset_mng
        self.portfolio = prt_mng
        self.type = None
        self.transactions = self.get_transactions()

    @staticmethod
    def get_transactions():
        err = ''
        data = {}

        if not os.path.exists(TRANSACTIONS_FILE):
            err = TRX_FILE_ERR
        else:
            try:
                with open(TRANSACTIONS_FILE) as file:
                    data = json.load(file)
                file.close()
            except json.JSONDecodeError:
                err = TRX_GET_ERR
        if err:
            display_err(err)

        return data

    def save_transactions(self):
        err = ''
        status = True
        if not os.path.exists(TRANSACTIONS_FILE):
            err = TRX_FILE_ERR
        else:
            try:
                with open(TRANSACTIONS_FILE, 'w') as file:
                    json.dump(self.transactions, file)
                file.close()
            except:
                err = TRX_UPDATE_ERR

        if err:
            status = False
            display_err(err)

        return status

    def get_next_id(self) -> str:
        err = ''
        next_id = None
        try:
            ids = [int(item) for item in self.transactions]
            if ids:
                max_id = max(ids)
                next_id = max_id + 1
            else:
                next_id = 1
        except:
            err = TRX_NEXT_ID

        if err:
            display_err(err)

        return str(next_id)

    def get_transactions_for_ticker(self, ticker):
        err = ''
        transactions = None

        try:
            transactions = [transaction for transaction in self.transactions.values(
            ) if transaction.get('symbol') == ticker]
        except:
            err = TRX_TRX_BY_TICKER

        if err:
            display_err(err)

        return transactions

    def get_performance(self) -> str:
        assets = AssetManager.get_assets()
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
        s_performance = {}
        for x, y in stock_performance.items():
            symbol = y.get('symbol')
            price = y.get('price')
            qty = y.get('quantity')
            cur_price = y.get('latest_price')['price']
            delta = cur_price / price
            buy_total += price * qty
            cur_total += cur_price * qty
            performance = {
                "buy_total":  price * qty,
                "cur_total":  cur_price * qty,
            }
            s_performance[symbol] = performance

        all_performance = {
            'total_buy': buy_total,
            'total_current': cur_total,
            'stocks': s_performance
        }

        return all_performance

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
                formatted_total = format_currency(total)
                formatted_price = format_currency(price)

                if action == OrderSide.BUY:
                    total = -1 * total

                # Generate message
                msg = f"\n    Submitting ({str(_type).upper()}) order to {action.value.upper()} {quantity} of {symbol} @ ${formatted_price} (total: ${formatted_total}).\n"

            except:
                err = TRX_MSG_CREATE_ERR
                status = False

        # Save assets
        if status:
            status = self.assets.update_assets(action, symbol, quantity)
        else:
            err = TRX_MSG_CREATE_ERR
            status = False

        # Update portfolio balance
        if status:
            status = self.portfolio.update_balance(total)
        else:
            status = False

        if status:
            # Save transaction
            self.transactions = temp_trx
            status = self.save_transactions()
        else:
            status = False

        if status:
            print(msg)
            return True
        else:
            err = TRX_SAVE_ERR

        print(err)
        return False
