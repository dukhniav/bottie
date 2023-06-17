import json
import os

from constants import display_err, BALANCE_LOW_ERR, BALANCE_UPDATE_ERR, BALANCE_GET_ERR, BALANCE_FILE_ERR, BALANCE_ROLLBACK

BALANCE_FILE_PATH = 'data/balance.json'


class PortfolioManager:
    def __init__(self):
        self.balance = self.get_balance()

    @staticmethod
    def get_balance() -> float:
        balance = float(0)
        err = ''
        if not os.path.exists(BALANCE_FILE_PATH):
            err = BALANCE_FILE_ERR
        else:
            try:
                with open(BALANCE_FILE_PATH) as file:
                    data = json.load(file)
                    balance = data['balance']
            except:
                err = BALANCE_GET_ERR

        if err:
            display_err(err)

        return balance

    def save_balance(self) -> bool:
        status = True
        err = ''

        new_balance = {
            'balance': self.balance
        }
        if not os.path.exists(BALANCE_FILE_PATH):
            err = BALANCE_FILE_ERR
        else:
            try:
                with open(BALANCE_FILE_PATH, 'w') as file:
                    json.dump(new_balance, file)
            except:
                err = BALANCE_UPDATE_ERR

        if err:
            status = display_err(err)

        return status

    def update_balance(self, trx_amt: float) -> bool:
        """update balance

        Args:
            trx_amt (float): amount to update balance by

        Returns: status
        """
        status = True
        err = ''

        buy = trx_amt < 0
        cur_balance = self.balance

        if buy:
            if cur_balance >= trx_amt:
                cur_balance += trx_amt
            else:
                err = BALANCE_LOW_ERR
        else:
            cur_balance += trx_amt

        if err:
            status = display_err(err)
        else:
            self.balance = cur_balance
            status = self.save_balance()

        return status

    def rollback_transaction(self, balance: float):
        self.balance = balance
        self.save_balance()
        display_err(BALANCE_ROLLBACK)
