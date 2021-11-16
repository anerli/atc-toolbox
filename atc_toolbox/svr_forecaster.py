from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from atc_toolbox.date_utils import date_range
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

		df = pd.DataFrame(
			data=y_pred,
			index=pd.DatetimeIndex(date_range(dates[0], dates[-1], self.calendar)),
			columns=self.y_feature_names
			)
		return df

	def predict_range(self, start_date, end_date):
		dates = date_range(start_date, end_date, self.calendar)
		# Technically no reason why this can't be the case, but seems silly
		if not dates[0] >= self.train_start_date:
			print(f'Error: Start date {start_date} below train start date {self.train_start_date}')
			exit(1)
		# TODO: Allow user to set calendar
		
		return self.predict(dates)

	def predict_train(self):
		return self.predict_range(self.train_start_date, self.train_end_date)
		
if __name__ == '__main__':
	import yfinance as yf
	import matplotlib.pyplot as plt
	from datetime import datetime

	start_date = datetime(2001, 1, 1)
	end_date = datetime(2010, 1, 1)

	df = yf.download('MSFT', start_date, end_date)

	print(df)

	# features = ['Adj Close', 'Open']
	features = ['Adj Close']

	train_end_date = datetime(2008, 1, 1)

	# Train only on a subset of the data
	df_train = df.loc[start_date:train_end_date,:]
	df_test = df.loc[train_end_date:,:]
	print(df_train)

	# Predictive cababilities are very limited because of this kernel
	# this is why we would like more advanced forecasting algorithms!
	forecaster = SVR_Forecaster(df_train, features, kernel='rbf')

	y_pred = forecaster.predict_range(start_date, end_date)
	print(y_pred)
	print(type(y_pred))

	ma50 = df[['Adj Close']].rolling(window=50).mean()
	ma200 = df[['Adj Close']].rolling(window=200).mean()

	plt.plot(ma50, label='50 day moving average')
	plt.plot(ma200, label='200 day moving average')
	for feature in features:
		
		plt.plot(df_train[[feature]], label=f'{feature} Train')
		plt.plot(df_test[[feature]], label=f'{feature} Test')
		plt.plot(y_pred[[feature]], label=f'{feature} SVR Forecast')

	plt.legend()
	plt.show()