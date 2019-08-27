
import yfinance as yf
import talib
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


# T : telegram
class ckTelegram:
    import telegram

    T_TOKEN = ""
    T_CHATID_CK = ""
    T_CHATID_GROUP = ""

    def __init__(s):
        s.bot = s.telegram.Bot(token=s.T_TOKEN)

    def send_message(s, id, message):
        s.bot.send_message(id, message)

    def send_message_ck(s, message):
        s.send_message(s.T_CHATID_CK, message)

    def send_message_group(s, message):
        s.send_message(s.T_CHATID_GROUP, message)


def getData():
    # https://github.com/ranaroussi/yfinance
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers=stock_code_list,
        # tickers="SPY AAPL MSFT",

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period="6mo",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval="1d",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by='ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust=True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost=True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        treads=True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy=None
    )
    return data


if __name__ == "__main__":

    RSI_NUM = 13
    # subscribe Kline

    stock_code_list = [
        "AMZN", "MSFT", "NEE", "WM", "KO", "AMT",
        "MA", "COST", "TQQQ", "VMW", "ABT"
    ]

    data = getData()

    text = '{:_<8}{:_<9}{:<9}\n'.format("Code", "RSI", "Close")

    for code in stock_code_list:
        rsi = talib.RSI(data[code]['Close'].fillna(method='ffill'))
        # data[code] = data[code].assign(rsi=rsi)
        t = '{:_<8}{:_<9.1f}{:<9.2f}\n'.format(code, rsi[-1], data.iloc[-1][code]['Close'])
        text += t
        print(t)

    # ckTelegram().send_message_group(text)
    ckTelegram().send_message_ck(text)
