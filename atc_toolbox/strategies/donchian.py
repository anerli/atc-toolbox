from backtesting import Backtest, Strategy
import pandas as pd

def don_max(arr: pd.Series, window: int) -> pd.Series:
	return pd.Series(arr).rolling(window).max()
def don_min(arr: pd.Series, window: int) -> pd.Series:
	return pd.Series(arr).rolling(window).min()

class Donchian(Strategy):
    window: int = 50
    momentum: bool = False
    def init(self):
        price = self.data.Close
        self.don_max_i = self.I(don_max, price, self.window)
        self.don_min_i = self.I(don_min, price, self.window)

    def next(self):
        # Similar to crossover except instead we check for equality.
        if self.data.Close[-1] == self.don_max_i[-1]:
            if self.momentum:
                self.buy()
            else:
                self.sell()
        elif self.data.Close[-1] == self.don_min_i[-1]:
            if self.momentum:
                self.sell()
            else:
                self.buy()

if __name__ == '__main__':
    import yfinance as yf
    df = yf.download('MSFT', '2011-1-1', '2012-12-31')
    bt = Backtest(df, Donchian, exclusive_orders=True)

    bt.run(momentum=False, window=100)

    bt.plot()
