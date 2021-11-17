import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
from atc_toolbox.svr_forecaster import SVR_Forecaster

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