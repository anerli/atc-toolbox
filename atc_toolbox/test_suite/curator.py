'''
Curator generates the ledger.csv used by acquirer.py to download data tables.
'''
import pandas as pd
from datetime import datetime

snp500 = pd.read_csv('SnP500.csv')

print(snp500.head())

# TODO: Produce a ledger.csv, containing cols TICKER, START_DATE, END_DATE

ledger = pd.DataFrame(columns=['Symbol', 'StartDate', 'EndDate'])

#ledger.iloc[[0]] = ['test1', 'test2', 'test3']
symbols = snp500['Symbol']
start_dates = [datetime(2000, 1, 1)]*len(symbols)
end_dates = [datetime(2021, 1, 1)]*len(symbols)


ledger['Symbol'] = snp500['Symbol']
ledger['StartDate'] = start_dates
ledger['EndDate'] = end_dates

# ledger[]

print(ledger.head())

ledger.to_csv('ledger.csv')