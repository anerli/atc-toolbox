'''
For accessing data and running test cases.
'''
#from atc_toolbox.test_suite.synchronizer import DATA_PATH, fname_to_values
from atc_toolbox.test_suite.manager import load, list_data, decompose_fname
import os
import pandas as pd
from backtesting import Backtest
from typing import List
import random

def test_list(Strategy: type, fnames: List[str], **kwargs):
    stats_list = []
    for fname in fnames:
        stats_list.append(test_one(Strategy, fname, **kwargs))
    return stats_list

def test_full(Strategy: type, **kwargs):
    # all_stats = []
    # for fname in list_data():
    #     all_stats.append(test_one(Strategy, fname, **kwargs))
    # return all_stats
    return test_list(Strategy, list_data(), **kwargs)



'''
Test a Strategy against a single data table.
'''
def test_one(Strategy: type, fname: str, backtest_kwargs={}, run_kwargs={}, verbose=False, plot=False):
    symbol, start_date, end_date = decompose_fname(fname)
    if verbose: print(f'Testing on {symbol} from {start_date} to {end_date}...')
    #df = pd.read_csv(os.path.join(DATA_PATH, fname))
    df = load(fname)
    #print(df.head())
    bt = Backtest(df, Strategy, **backtest_kwargs)
    bt_stats = bt.run(**run_kwargs)
    # bt_stats is a pd.Series
    #print(type(bt_stats))
    #print(bt_stats)
    if plot: bt.plot()
    return bt_stats

def test_random(Strategy: type, n: int, **kwargs):
    sample_fnames = []
    all_fnames = list_data()
    for _ in range(n):
        sample = random.choice(all_fnames)
        sample_fnames.append(sample)
        all_fnames.remove(sample)
    return test_list(Strategy, sample_fnames, **kwargs)

def summarize(stats_list = List[pd.Series]):
    avg_return = sum([stats['Return [%]'] for stats in stats_list]) / len(stats_list)
    print('Average Return [%]:', avg_return)

# Run over all test files with given ticker symbols
def test_symbols(symbols):
    pass