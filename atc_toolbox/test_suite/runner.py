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

def test_list(Strategy: type, fnames: List[str], verbose=False, **kwargs):
    if len(fnames) == 0:
        raise Exception('At least one file to test must be provided.')
    stats_list = []
    for i, fname in enumerate(fnames):
        symbol, start_date, end_date = decompose_fname(fname)
        if verbose: print(f'({i+1}/{len(fnames)}) Testing on {symbol} from {start_date} to {end_date}...')
        stats = test_one(Strategy, fname, **kwargs)
        if not isinstance(stats, type(None)): stats_list.append(stats)

    return stats_list

def test_full(Strategy: type, **kwargs):
    return test_list(Strategy, list_data(), **kwargs)

'''
Test a Strategy against a single data table.
'''
def test_one(Strategy: type, fname: str, backtest_kwargs={}, run_kwargs={}, verbose=False, plot=False):
    df = load(fname)
    bt = Backtest(df, Strategy, **backtest_kwargs)

    try:
        bt_stats = bt.run(**run_kwargs)
    except Exception as e:
        print(f'Caught {e.__class__.__name__} exception while running file {fname}, tossing out this result.')
        return
    
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
    if len(stats_list) == 0:
        print('Cannot summary empty stats list.')
        return
    avg_return = sum([stats['Return [%]'] for stats in stats_list]) / len(stats_list)
    print('Average Return [%]:', avg_return)

# Run over all test files with given ticker symbols
def test_symbols(Strategy: type, symbols: List[str], **kwargs):
    symbols = set(symbols)
    fnames = []
    for fname in list_data():
        symbol, _, _ = decompose_fname(fname)
        if symbol in symbols:
            fnames.append(fname)
    if not fnames:
        raise Exception(f'No matching filenames for symbols {symbols} found.')
    return test_list(Strategy, fnames, **kwargs)
