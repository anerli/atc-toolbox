import yfinance as yf

class YFDF:
	'''
	Wrapper class for a pandas dataframe obtained via the yfinance package.
	Purpose is to enforce required columns and make them easier to access,
	as well as providing some common methods.
	'''
	def __init__(self, df):


	@classmethod
	def from_yf(cls, *args, **kwargs):
		return cls()