import finnhub


class Finnhub:
    def __init__(self, api_key: str) -> None:
        # Setup client
        self.client = finnhub.Client(api_key=api_key)


import finnhub

# Setup client
finnhub_client = finnhub.Client(api_key="YOUR API KEY")

# Stock candles
res = finnhub_client.stock_candles("AAPL", "D", 1590988249, 1591852249)
print(res)
