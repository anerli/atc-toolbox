import pandas as pd
import os

DATA_PATH = './data'

def row_to_fname(symbol: str, start_date: str, end_date: str):
    return symbol + '_' +  start_date + '_' + end_date + '.csv'

def fname_to_row(fname: str):
    # Cut off '.csv'
    fname = fname[:-4]
    symbol, start_date, end_date = fname.split('_')
    return symbol, start_date, end_date

def download(ledger):
    # Download all data specified in the ledger
    pass

def check_data(ledger):
    # Compare ledger against downloaded tables
    missing = check_missing(ledger)
    excess = check_excess(ledger)
    pass

def check_missing(ledger):
    missing = set()
    for index, row in ledger.iterrows():
        missing.add(row_to_fname(row['Symbol'], row['StartDate'], row['EndDate']))
    for f in os.listdir(DATA_PATH):
        # discard: like remove but no error if element not in set
        missing.discard(f)
    return missing   

def check_excess(ledger):
    excess = set()
    for f in os.listdir(DATA_PATH):
        excess.add(f)
    for index, row in ledger.iterrows():
        fname = row_to_fname(row['Symbol'], row['StartDate'], row['EndDate'])
        excess.discard(fname)
    return excess

if __name__ == '__main__':
    # TODO: Download curated datasets
    ledger = pd.read_csv('ledger.csv')
    #print(type(ledger.iloc[0,2]))
    symbol, start, end = fname_to_row('ABBV_2000-01-01_2021-01-01.csv')
    print(symbol, start, end)
    print(row_to_fname(symbol, start, end))
    download(ledger)

    #print(check_missing(ledger))
    print('Num missing files:', len(check_missing(ledger)))
    print('Num excess files:', len(check_excess(ledger)))