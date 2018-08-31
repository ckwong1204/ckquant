
from futuquant import *
import pandas as pd
import talib


def get_DF_RSI():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # ret, data = quote_ctx.get_history_kline('US.AMZN', start='2017-01-01', end='2018-08-17', ktype='K_30M')
    ret, data = quote_ctx.get_cur_kline('US.AMZN', 1000, SubType.K_60M, AuType.QFQ)
    quote_ctx.close()
    if ret == RET_OK:
        data['rsi13'] = talib.RSI(data['close'],13)
        return data


def saveToCsv():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['US.AMZN'], [SubType.K_30M])
    ret, data = quote_ctx.get_history_kline('US.AMZN', start='2017-01-01', end='2019-01-01', ktype='K_30M')
    quote_ctx.close()
    if ret == RET_OK:
        data.to_csv('amzn_30M_201701_201708.csv')
        print( 'csv printed' )


def loadCsv():
    df = pd.read_csv('amzn_30M_201701_201708.csv')
    # pd.read_csv('amzn.csv', parse_dates=True)
    return df

    # for col in c[1].columns:
    #     print(col, c[1][col].equals(d[col]))

    # import os
    # os.getcwd()  # 获取当前工作路径


def futubase():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['US.AMZN'], [SubType.K_60M])
    c = quote_ctx.get_cur_kline('US.AMZN', 1000, SubType.K_60M, AuType.QFQ)
    d = quote_ctx.get_history_kline('US.AMZN', start='2018-03-05', end='2018-07-29', ktype='K_DAY')
    quote_ctx.close()

# def analyseRSI()

def addDateTime(df):
    date_time = df['time_key'].str.split(expand=True)
    df['time_key_day'] = date_time[0]
    df['time_key_min'] = date_time[1]
    return df

def filterRSI():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['US.AMZN'], [SubType.K_60M])
    ret, df = quote_ctx.get_cur_kline('US.AMZN', 1000, SubType.K_60M, AuType.QFQ)
    quote_ctx.close()
    if ret == RET_OK:
        df['rsi13'] = talib.RSI(df['close'], 13)
        # return data

        buyList = df[(df.rsi13 < 30)]
        buyList = addDateTime(buyList)
        # buyList_day = buyList.drop_duplicates('time_key_day', 'first')

        # for index, row in df[(df.rsi13 < 20)].iterrows():
        #     print(row['rsi13'])

        # df[len(df), :]
        return buyList;



if __name__ == "__main__":
    # futubase()

    # saveToCsv()
    # csv = loadCsv()

    # df = addRSI()

    # df = filterRSI()
    # df

    import futuquant as ft
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # subscribe Kline
    stock_code_list = ["US.AAPL", "HK.00700"]
    sub_type_list = [ft.SubType.K_1M, ft.SubType.K_5M, ft.SubType.K_15M, ft.SubType.K_30M, ft.SubType.K_60M,
                     ft.SubType.K_DAY, ft.SubType.K_WEEK, ft.SubType.K_MON]

    ret_status, ret_data = quote_ctx.subscribe(stock_code_list, sub_type_list)
    if ret_status != ft.RET_OK:
        print(ret_data)
        exit()

    ret_status, ret_data = quote_ctx.query_subscription()
    if ret_status == ft.RET_ERROR:
        print(ret_data)
        exit()
    print(ret_data)

    for code in stock_code_list:
        for ktype in [ft.SubType.K_DAY, ft.SubType.K_1M, ft.SubType.K_5M]:
            ret_code, ret_data = quote_ctx.get_cur_kline(code, 5, ktype)
            if ret_code == ft.RET_ERROR:
                print(code, ktype, ret_data)
                exit()
            kline_table = ret_data
            print("%s KLINE %s" % (code, ktype))
            print(kline_table)
            print("\n\n")

