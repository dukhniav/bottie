import json
import os

from typing import Dict

from finnhub_api import finnhub_api

from enums import OrderSide, OrderType

ASSETS_FILE = 'data/assets.json'


class AssetManager:
    def __init__(self):
        self.assets = self.load_assets()

    @staticmethod
    def get_assets():
        assets: Dict = AssetManager.load_assets()
        msg = None

        if assets:
            msg = f'Currently owned assets:'
            for asset in assets:
                msg += '\n' + ' ' * 4 + \
                    asset + ' - ' + str(assets[asset]['quantity'])
        else:
            msg = 'No owned assets.'

        return msg

    @staticmethod
    def load_assets():
        data = {}
        if os.path.exists(ASSETS_FILE):
            try:
                with open(ASSETS_FILE) as file:
                    data = json.load(file)
                file.close()
            except json.JSONDecodeError:
                return data

        return data

    def save_assets(self):
        with open(ASSETS_FILE, 'w') as file:
            json.dump(self.assets, file, indent=4)
        file.close()

    def update_assets(self, side: OrderSide, symbol: str, quantity: int) -> bool:
        status = None
        if side == OrderSide.BUY:
            status = self.add_asset(symbol, quantity)
        else:
            status = self.remove_asset(symbol, quantity)
        return status

    def add_asset(self, symbol, quantity) -> bool:
        try:
            if symbol in self.assets:
                self.assets[symbol]['quantity'] += quantity
            else:
                asset = {}
                asset['quantity'] = quantity
                self.assets[symbol] = asset

            self.save_assets()
            return True
        except:
            return False

    def remove_asset(self, symbol, quantity) -> bool:
        status = True
        try:
            print(f'sym: {symbol}, qty: {quantity}')
            if symbol in self.assets:
                if self.assets[symbol]['quantity'] >= quantity:
                    self.assets[symbol]['quantity'] -= quantity
                    if self.assets[symbol]['quantity'] == 0:
                        del self.assets[symbol]
                    self.save_assets()

                else:
                    print(f"You don't have enough {symbol} to sell.")
                    status = False
            else:
                print(f"You don't own any {symbol}.")
                status = False
        except:
            status = False
        return status
