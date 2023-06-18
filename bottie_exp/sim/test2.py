import pandas as pd

from strategy2 import Strategy
# Assuming you already have the Strategy class defined


def test_strategy(strategy: Strategy, data, starting_balance=10000):
    print('in func')
    portfolio = {'balance': starting_balance, 'shares': 0}
    buy_price = 0
    sell_price = 0

    data = strategy.analyze_data(data)
    for i in range(len(data)):
        signal = data.loc[i, 'Signal']
        close_price = data.loc[i, 'c']
        if signal != 'Hold':
            print(f'{i} - {close_price} - {signal}')
        if signal == 'Buy' and portfolio['balance'] > 0:
            shares_to_buy = portfolio['balance'] / close_price
            portfolio['shares'] += shares_to_buy
            buy_price = close_price
            portfolio['balance'] -= buy_price * shares_to_buy

            print(
                f'Buying {shares_to_buy} @ {buy_price} ==> ${shares_to_buy * buy_price}. Left: ${portfolio["balance"]}')

        elif signal == 'Sell' and portfolio['shares'] > 0:
            portfolio['balance'] += portfolio['shares'] * close_price
            portfolio['shares'] = 0
            sell_price = close_price

        if buy_price != 0 and sell_price != 0:
            profit = portfolio['balance'] - starting_balance
            print(f"Buy @ {buy_price}, Sell @ {sell_price}, Profit: {profit}")
            buy_price = 0
            sell_price = 0

    if portfolio['shares'] > 0:
        portfolio['balance'] += portfolio['shares'] * close_price

    return portfolio['balance'] - starting_balance
