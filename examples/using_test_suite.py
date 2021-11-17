from atc_toolbox.test_suite.runner import test_full, test_one, summarize, test_random, test_symbols
from atc_toolbox.strategies.crossover import SmaCross
from backtesting import Backtest

'''
# Say you wanted parameters like this:
bt_sma = Backtest(df, SmaCross, exclusive_orders=True)
bt_sma.run(momentum=False, window_short=10, window_long=100)
'''

stats_list = test_full(
    SmaCross,
    backtest_kwargs={'exclusive_orders': True},
    run_kwargs={'momentum': False, 'window_short': 10, 'window_long': 100},
    verbose=True
)

# stats_list = test_random(
#     SmaCross,
#     5,
#     backtest_kwargs={'exclusive_orders': True},
#     run_kwargs={'momentum': False, 'window_short': 10, 'window_long': 100},
#     verbose=True
# )

# stats_list = test_symbols(
#     SmaCross,
#     ['OGN'],
#     backtest_kwargs={'exclusive_orders': True},
#     run_kwargs={'momentum': False, 'window_short': 10, 'window_long': 100},
#     verbose=True
# )

summarize(stats_list)