# https://pythonprogramming.net/regression-introduction-machine-learning-tutorial/?completed=/machine-learning-tutorial-python-introduction/

import pandas as pd
import quandl, math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
from datetime import datetime, timedelta


# ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio',
#        'turnover_rate', 'volume', 'turnover', 'change_rate', 'last_close']
CLOSE = 'close'
HIGH = 'high'
OPEN = 'open'
LOW = 'low'
VOLUME = 'volume'
TIME_KEY = 'time_key'


def getDataFromFutu(code='US.AMZN', start='2010-01-01'):
    import futuquant as ft
    quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.get_history_kline(code, start, end='2099-01-01', ktype='K_DAY')
    return data

style.use('ggplot')

df = getDataFromFutu(code='US.AMZN', start='2010-01-01')

print(df.tail())

df = df[[OPEN, HIGH, LOW, CLOSE, VOLUME, TIME_KEY]]
df.set_index(TIME_KEY, inplace=True)
df['HL_PCT'] = (df[HIGH] - df[LOW]) / df[CLOSE] * 100.0
df['PCT_change'] = (df[CLOSE] - df[OPEN]) / df[OPEN] * 100.0

df = df[[CLOSE, 'HL_PCT', 'PCT_change', VOLUME]]
print(df.tail())

forecast_col = CLOSE
df.fillna(value=-99999, inplace=True)
# forecast_out = int(math.ceil(0.01 * len(df)))  # 10 percent of the data
forecast_out = 13
print("forecast_out: ", forecast_out)

df['label'] = df[forecast_col].shift(-forecast_out)

df_org = df

X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

df.dropna(inplace=True)

y = np.array(df['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)


# accuracy
# algorithm  https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
# clf = svm.SVR()
# clf = LinearRegression()
clf = LinearRegression(n_jobs=-1) #-1 means using all processors
clf.fit(X_train, y_train)
# with open('linearregression.pickle','wb') as f:
#     pickle.dump(clf, f)
#
# pickle_in = open('linearregression.pickle', 'rb')
# clf = pickle.load(pickle_in)

confidence = clf.score(X_test, y_test)
print("LinearRegression:", confidence)

# accuracy of the other regression model
## for k in ['linear','poly','rbf','sigmoid']:
##     clf = svm.SVR(kernel=k)
##     clf.fit(X_train, y_train)
##     confidence = clf.score(X_test, y_test)
##     print(k,confidence)

forecast_set = clf.predict(X_lately)
print(forecast_set, confidence, forecast_out)

df_org['Forecast'] = np.nan

last_date = df_org.iloc[-1].name
last_datetime = datetime.strptime(str(last_date), "%Y-%m-%d %H:%M:%S")
one_day = timedelta(days=1)
mins_30 = timedelta(minutes=30)
next_datetime = last_datetime + timedelta(days=1) - timedelta(hours=6)

for i in forecast_set:
    next_date_str = next_datetime.strftime("%Y-%m-%d %H:%M:%S")
    next_datetime += mins_30
    df_org.loc[next_date_str] = [np.nan for _ in range(len(df_org.columns) - 1)] + [i]

print(df_org.iloc[-26:])

# plot lost 50 date data
# df_org.iloc[-13:][CLOSE].plot()
df_org.iloc[-13:]['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()