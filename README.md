# ATC Toolbox
ATC Toolbox was written by members of Algorithmic Trading Club at ISU and is meant for use by ATC members, as well as anyone else who feels like using it. 

This is a set of tools that can be used for financial data analysis, for use in trading algorithms, and whatever else you might desire to use it for.

## I'm a noob, how do I use this?

Normally you install modules with `pip install packagename`, however since this is not on pypi (the pip package repository), you have to install it slightly differently.

Clone (or just download if you want) this repository, and (assuming you are running a terminal in the parent directory of this repository) `pip install -e atc-toolbox`. Then you will be able to access the `atc_toolbox` module from python. The -e flag means that when you pull new changes from atc-toolbox the changes will be automatically reflected without having to pip re-install it.

## Docs
- There are no docs for this yet :(
- For now look at the code to see what stuff does.

## Example Usage

```py
from atc_toolbox.svr_forecaster import SVR_Forecaster

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

start_date = datetime(2008, 1, 1)
end_date = datetime(2010, 1, 1)

# Download financial data as pandas dataframe
df = yf.download('MSFT', start_date, end_date)

# Features to forecast
# (if number of features is greater than 1, each feature will be used to train a different submodel)
features = ['Adj Close']

# Initialize (and train) an SVR Forecaster.
forecaster = SVR_Forecaster(df, features, kernel='rbf')

# Plot real data
plt.plot(df['Adj Close'])
# Plot SVR forecast
plt.plot(forecaster.predict_train())

# Show plot
plt.show()
```