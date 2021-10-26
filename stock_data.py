import yfinance as yf

class StockData:
	'''
	A wrapper class for a pandas dataframe.
	Enforces the existence of certain columns,
	and provides some commonly used methods.
	'''
	def __init__(self, df):
		# TODO: Verify existence of certain columns
		self.df = df

	@classmethod
	def from_yf(cls, *args, **kwargs):
		'''
		Create an instance given arguments to a call
		to yfinance.download().
		'''
		return cls(yf.download(*args, **kwargs))

	@property
	def adj_close(self):
		return self.df['Adj Close']