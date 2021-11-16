'''
Should be the only python script to directly access and manage the data files.
'''
import pandas as pd
import os
from typing import List
import yfinance as yf

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
LEDGER_PATH = os.path.join(SCRIPT_PATH, 'ledger.csv')
DATA_PATH = os.path.join(SCRIPT_PATH, 'data')

def list_data():
    return os.listdir(DATA_PATH)

def load_ledger() -> pd.DataFrame:
    return pd.read_csv(LEDGER_PATH)

def save_ledger(ledger: pd.DataFrame):
    ledger.to_csv(LEDGER_PATH)

def load(fname: str) -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA_PATH, fname))
    df.index = pd.to_datetime(df.index)
    return df

def row_to_fname(row: pd.Series): #symbol: str, start_date: str, end_date: str
    symbol, start_date, end_date = row['Symbol'], row['StartDate'], row['EndDate']
    return symbol + '_' +  start_date + '_' + end_date + '.csv'

def decompose_fname(fname: str):
    # Cut off '.csv'
    fname = fname[:-4]
    symbol, start_date, end_date = fname.split('_')
    return symbol, start_date, end_date

def download_missing(missing: List[str]):
    # Download all data specified in the ledger
    for fname in missing:
        symbol, start_date, end_date = decompose_fname(fname)
        print(f'Downloading {symbol} from {start_date} to {end_date}...')
        df = yf.download(symbol, start_date, end_date)
        df.to_csv(os.path.join(DATA_PATH, fname))
    print('All files downloaded.')

def remove_excess(excess: List[str]):
    for fname in excess:
        os.remove(os.path.join(DATA_PATH, fname))

def get_missing(ledger: pd.DataFrame):
    missing = set()
    for index, row in ledger.iterrows():
        missing.add(row_to_fname(row))
    for f in os.listdir(DATA_PATH):
        # discard: like remove but no error if element not in set
        missing.discard(f)
    return list(missing)

def get_excess(ledger: pd.DataFrame):
    excess = set()
    for f in os.listdir(DATA_PATH):
        excess.add(f)
    for index, row in ledger.iterrows():
        fname = row_to_fname(row)
        excess.discard(fname)
    return list(excess)
