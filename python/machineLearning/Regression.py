# https://pythonprogramming.net/regression-introduction-machine-learning-tutorial/?completed=/machine-learning-tutorial-python-introduction/

import pandas as pd
import quandl, math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

df = quandl.get("WIKI/GOOGL")

print(df.head())

df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
print(df.head())

forecast_col = 'Adj. Close'
df.fillna(value=-99999, inplace=True)
# forecast_out = int(math.ceil(0.01 * len(df)))  # 10 percent of the data
forecast_out = 20
print("forecast_out: ", forecast_out)

df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)

X = np.array(df.drop(['label'], 1))
y = np.array(df['label'])

X = preprocessing.scale(X)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)



# algorithm  https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
# clf = svm.SVR()
# clf = LinearRegression()
clf = LinearRegression(n_jobs=-1) #-1 means using all processors
clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)
print("LinearRegression:",confidence)

for k in ['linear','poly','rbf','sigmoid']:
    clf = svm.SVR(kernel=k)
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print(k,confidence)

