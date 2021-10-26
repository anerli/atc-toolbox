from sklearn.svm import SVR

class SVR_Forecaster:
    def __init__(self, yf_df, *SVR_args, **SVR_kwargs):
        self.df = yf_df.copy()
        # End time index (exclusive) for train period
        self.t_end = self.df.shape[0]
        # Add column for integer time step
        self.df['TimeIndex'] = [i for i in range(self.t_end)]
        train_X = self.df[['TimeIndex']]
        train_Y = self.df[['Adj Close']]
        print(train_X)
        self.model = SVR(*SVR_args, **SVR_kwargs)
        self.model.fit(train_X, train_Y)

    # TODO: Need to be able to covert from time index back to datetime, for plotting and such
    # Returned predictions should be dataframes indexed by datetime

    # Return predictions over the training interval
    def predict_train(self):
        time_indices = list(range(0, self.t_end))
        time_indices_dim_fix = [[t] for t in time_indices]
        return self.model.predict(time_indices_dim_fix)


    # dt: Number of time units past the end of the training data
    def predict(self, dt):
        time_indices = list(range(self.df.shape[0], self.df.shape[0] + dt))
        time_indices_dim_fix = [[t] for t in time_indices]
        return self.model.predict(time_indices_dim_fix)

    #def plot()

if __name__ == '__main__':
    import yfinance as yf
    import matplotlib.pyplot as plt

    df = yf.download('MSFT', '2015-01-01', '2020-01-01')

    forecaster = SVR_Forecaster(df)
    print(forecaster.df)
    y_pred = forecaster.predict_train()
    print(y_pred)

    plt.plot(df['Adj Close'])
    plt.plot(y_pred)
    plt.show()
    #print(forecaster.predict(10))
