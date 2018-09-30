from matplotlib import style
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web


#########################
# # download as tsla.csv
def save_to_csv():
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2018, 9, 28)

    df = web.DataReader('TSLA', 'yahoo', start, end)
    df.to_csv('tsla.csv')


#########################
# # read tsla.csv, and plot grath
def show_graph():
    style.use('ggplot')
    df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
    df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()

    print(df.head())
    # df['Adj Close'].plot()
    # plt.show()

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

    ax1.plot(df.index, df['Adj Close'])
    ax1.plot(df.index, df['100ma'])
    ax2.bar(df.index, df['Volume'])

    plt.show()


#########################
# # read tsla.csv, and plot grath
# from mpl_finace import candlestick_ohlc ## pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
def plot_ohlc_graph():
    import matplotlib.dates as mdates
    from mpl_finance import candlestick_ohlc

    style.use('ggplot')
    df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

    plt.show()


def save_sp500_tickers():
    import bs4 as bs

    import pickle
    import requests

    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers


def get_data_from_yahoo(reload_sp500=False):
    import datetime as dt
    import os
    import pickle
    import pandas as pd
    import pandas_datareader.data as web
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2016, 12, 31)

    for ticker in tickers[:10]:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

    return tickers


def compile_data():
    import pickle
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    for count, ticker in list(enumerate(tickers))[:10]:
        print(count, ticker)
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

    main_df.to_csv('sp500_joined_closes.csv')
    return main_df

def visulize_data():
    import pandas as pd
    import numpy as np
    df = pd.read_csv('sp500_joined_closes.csv')
    # df['MMM'].plot()
    # plt.show()
    df_corr = df.corr()

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_lables = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_lables)
    ax.set_ylabel(row_labels)

    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)

    plt.tight_layout()
    plt.show()



# save_sp500_tickers()
# tickers = get_data_from_yahoo()

# main_df = compile_data()
visulize_data()