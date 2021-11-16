from atc_toolbox.test_suite.accessor import test_full, test_one
from atc_toolbox.strategies.crossover import SmaCross
from backtesting import Backtest

'''
# Say you wanted parameters like this:
bt_sma = Backtest(df, SmaCross, exclusive_orders=True)
bt_sma.run(momentum=False, window_short=10, window_long=100)
'''

stats = test_one(
    SmaCross,
    'AAPL_2000-01-01_2021-01-01.csv',
    backtest_kwargs={'exclusive_orders': True},
    run_kwargs={'momentum': False, 'window_short': 10, 'window_long': 100},
    verbose=True
)
