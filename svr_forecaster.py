from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from date_utils import date_range
import pandas_market_calendars as mcal
import pandas as pd

# TODO: May want to inherit from a Forecaster base class
class SVR_Forecaster:
	'''
	df: Dataframe to forecast. Must have a pd.DateIndex index.
	feature: y feature column in df to predict.
	SVR_args: args to pass to SVR model.
	SVR_kwargs: kwargs to pass to SVR model.
	'''
	def __init__(self, df, features, *SVR_args, **SVR_kwargs):
		self.train_start_date = df.index[0].to_pydatetime()
		self.train_end_date = df.index[-1].to_pydatetime()

		self.calendar = mcal.get_calendar('NYSE')

		self.y_feature_names = features

		self.x_train = pd.DataFrame(index=df.index)
		# Column name below doesn't actually matter
		self.x_train['Days Since Train Start'] = [(df.index[i].to_pydatetime() - df.index[0].to_pydatetime()).days for i in range(df.shape[0])]
		self.y_train = df[features]

		svr_model = SVR(*SVR_args, **SVR_kwargs)
		self.model = MultiOutputRegressor(svr_model)
		self.model.fit(self.x_train, self.y_train)

	def predict(self, dates):
		dates_days_from_train_start = [(date - self.train_start_date).days for date in dates]
		x_dim_fix = [[date] for date in dates_days_from_train_start]
		y_pred = self.model.predict(x_dim_fix)
		#df = pd.DataFrame(index=pd.DatetimeIndex(date_range(dates[0], dates[1], self.calendar)))
		#df['Adj Close'] = y_pred

		#df = pd.DataFrame(index=pd.DatetimeIndex(date_range(dates[0], dates[-1], self.calendar)))
		#df[self.y_feature_name] = y_pred
		#return df

		df = pd.DataFrame(
			data=y_pred,
			index=pd.DatetimeIndex(date_range(dates[0], dates[-1], self.calendar)),
			columns=self.y_feature_names
			)
		#df[self.y_feature_name] = y_pred
		return df
		#return y_pred

	def predict_range(self, start_date, end_date):
		# Technically no reason why this can't be the case, but seems silly
		assert start_date >= self.train_start_date
		# TODO: Allow user to set calendar
		dates = date_range(start_date, end_date, self.calendar)
		return self.predict(dates)

	def predict_train(self):
		return self.predict_range(self.train_start_date, self.train_end_date)
		
if __name__ == '__main__':
	import yfinance as yf
	import matplotlib.pyplot as plt

	df = yf.download('MSFT', '2015-01-01', '2020-01-01')

	print(df)

	# features = ['Adj Close', 'Open']
	features = ['Adj Close']

	forecaster = SVR_Forecaster(df, features)
	#print(forecaster.df)
	y_pred = forecaster.predict_train()
	print(y_pred)
	print(type(y_pred))

	#plt.plot(df[[feature]])
	#for feature in features:

	for feature in features:
		plt.plot(df[[feature]], label=f'{feature} Actual')
		plt.plot(y_pred[[feature]], label=f'{feature} SVR Forecast')

	#plt.plot(df[features])
	#plt.plot(y_pred)
	#df[features].plot()
	#y_pred.plot()
	plt.legend()
	plt.show()