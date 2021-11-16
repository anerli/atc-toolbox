'''
For accessing data and running test cases.
'''
#from atc_toolbox.test_suite.synchronizer import DATA_PATH, fname_to_values
from atc_toolbox.test_suite.synchronizer import load, iterate_files, fname_to_values
import os
import pandas as pd
from backtesting import Backtest

def test_full(Strategy: type, backtest_kwargs={}, run_kwargs={}, verbose=False):
    for fname in iterate_files():
        test_one(Strategy, fname, backtest_kwargs, run_kwargs, verbose)

def test_one(Strategy: type, fname: str, backtest_kwargs={}, run_kwargs={}, verbose=False):
    symbol, start_date, end_date = fname_to_values(fname)
    if verbose: print(f'Testing on {symbol} from {start_date} to {end_date}...')
    #df = pd.read_csv(os.path.join(DATA_PATH, fname))
    df = load(fname)
    bt = Backtest(df, Strategy, **backtest_kwargs)
    bt_stats = bt.run(**run_kwargs)
    print(type(bt_stats))
    print(bt_stats)

# Run over all test files with given ticker symbols
def test_symbols(symbols):
    pass