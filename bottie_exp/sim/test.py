import os
import json
import datetime
import time
from datetime import date
from dateutil.relativedelta import relativedelta

import pandas as pd
from test2 import test_strategy

from strategy2 import Strategy
from finnhub_api import finnhub_api
FILE_PATH = 'data/historical/'


def get_file_names(directory):
    file_names = []
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            file_names.append(file_name)
    return file_names


def main():
    # strategy = Strategy()
    # with open(FILE_PATH)as file:
    #     data = json.load(file)
    # file.close()

    # for k, v in data.items():
    #     print(k, v)
    # ticks = ['SOFI', 'NIO']
    # timeframe = 5
    # to = date.today()
    # _from = to + relativedelta(months=-1)
    # to_u = int(time.mktime(to.timetuple()))
    # _from_u = int(time.mktime(_from.timetuple()))

    # for t in ticks:
    #     print(f'Retrvieving {t} stock data...', end='')
    #     data = finnhub_api.get_historical_data(t, timeframe, _from_u, to_u)

    #     file_path = FILE_PATH + 'historical_' + t + '_' + \
    #         str(timeframe) + 'min_' + str(_from) + '_' + str(to) + '.json'
    #     with open(file_path, 'w') as file:
    #         json.dump(data, file)
    #     file.close()
    #     print('done')

    directory_path = 'data/historical'  # Replace with the actual directory path
    files = get_file_names(directory_path)

    strategy = Strategy()

    with open('data/historical/historical_SOFI_5min_2023-05-17_2023-06-17.json') as file:
        data = json.load(file)
    file.close()

    analyzed_data = strategy.analyze_data(data)

    # rsi_values = analyzed_data['RSI']
    # ma_values = analyzed_data['MA']
    # signals = analyzed_data['Signal']

    # print(rsi_values)

    data = pd.read_json(
        'data/historical/historical_NIO_5min_2023-05-17_2023-06-17.json')
    print('entering')
    data = test_strategy(strategy, data, 1000)
    print(data)


if __name__ == '__main__':
    main()
