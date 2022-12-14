import numpy as np


class Generator:
    def __init__(self, trend, volatility):
        self.trend = trend
        self.volatility = volatility

    def generate_stock_price(self, last_price):
        price = last_price + self.trend + (1 + np.random.normal(0, self.volatility))
        price = round(price, 2)
        return price
