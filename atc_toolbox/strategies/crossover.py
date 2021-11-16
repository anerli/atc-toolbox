from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class CrossOver(Strategy):
    # Mean-reversion or momentum
    momentum: bool = False
    def init(self):
        if not hasattr(self, 'short') or not hasattr(self, 'long'):
            raise Exception('Please setup indicators self.short and self.long, and then call super().init()')

        if self.momentum:
            self.crossover_buy = self.short
            self.crossover_sell = self.long
        else:
            self.crossover_buy = self.long
            self.crossover_sell = self.short
    
    def next(self):
        if crossover(self.crossover_buy, self.crossover_sell):
            self.buy()
        elif crossover(self.crossover_sell, self.crossover_buy):
            self.sell()

class SmaCross(CrossOver):
    window_short: int = 20
    window_long: int = 50
    def init(self):
        assert self.window_short < self.window_long
        price = self.data.Close
        self.short = self.I(SMA, price, self.window_short)
        self.long = self.I(SMA, price, self.window_long)
        super().init()

if __name__ == '__main__':
    import yfinance as yf
    df = yf.download('MSFT', '2011-1-1', '2012-12-31')
    bt_sma = Backtest(df, SmaCross, exclusive_orders=True)

    bt_sma.run(momentum=False, window_short=10, window_long=100)

    bt_sma.plot()
