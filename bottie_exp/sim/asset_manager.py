import json
import os

from typing import Dict

from finnhub_api import finnhub_api

from enums import OrderSide, OrderType

from constants import display_err, ASSET_FILE_ERR, ASSET_GET_ERR, ASSET_UPDATE_ERR, ASSET_ROLLBACK
ASSETS_FILE = 'data/assets.json'


class AssetManager:
    def __init__(self):
        self.assets = self.get_assets()

    @staticmethod
    def get_assets() -> Dict:
        err = ''
        data = {}
        if not os.path.exists(ASSETS_FILE):
            err = ASSET_FILE_ERR
        else:
            try:
                with open(ASSETS_FILE) as file:
                    data = json.load(file)
                file.close()
            except json.JSONDecodeError:
                err = ASSET_GET_ERR

        if err:
            display_err(err)
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

    def rollback_transaction(self, assets):
        self.assets = assets
        self.save_assets()
        display_err(ASSET_ROLLBACK)
