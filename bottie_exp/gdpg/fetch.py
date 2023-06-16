import requests
import json
import os

OUTPUT_FILE = 'stock_data.json'
CREDENTIALS_FILE = 'credentials.json'


def load_best_params(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def get_api_key():
    with open(CREDENTIALS_FILE, 'r') as file:
        data = json.load(file)
    file.close

    return data['alphavantage']


def fetch_stock_data(ticker, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={api_key}"
    print(f"Fetching stock data for {ticker}...")
    response = requests.get(url)
    data = response.json()
    stock_data = data["Time Series (Daily)"]
    return stock_data


def save_stock_data(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file)
    print(f"Stock data saved to {output_file}")


def main():
    ticker = "AAPL"  # Example stock ticker
    stock_data = fetch_stock_data(ticker, get_api_key())
    save_stock_data(stock_data, OUTPUT_FILE)


if __name__ == '__main__':
    main()
