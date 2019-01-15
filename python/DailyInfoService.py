import futu as ft
import pandas as pd
import talib

from python import CkTelegram

RSI_NUM = 14

stock_code_list = ["US.AMZN",
                   "HK.00003",
                   "HK.00006",
                   "HK.00066",
                   "HK.00270",
                   "HK.00388",
                   "HK.00700",
                   "HK.00823",
                   "HK.02638"
                   ]
sub_type_list = [ft.SubType.K_1M,
                 ft.SubType.K_5M,
                 ft.SubType.K_15M,
                 ft.SubType.K_30M,
                 ft.SubType.K_60M,
                 ft.SubType.K_DAY,
                 ft.SubType.K_WEEK,
                 ft.SubType.K_MON]

def _example_cur_kline(quote_ctx):
    """
    获取当前K线，输出 股票代码，时间，开盘价，收盘价，最高价，最低价，成交量，成交额
    """
    ret_status, ret_data = quote_ctx.subscribe(stock_code_list, sub_type_list)
    if ret_status != ft.RET_OK:
        print(ret_data)
        exit()

    ret_status, ret_data = quote_ctx.query_subscription()
    if ret_status == ft.RET_ERROR:
        print(ret_data)
        exit()
    print(ret_data)

    resultList = []

    for code in stock_code_list:
        for ktype in [ft.SubType.K_WEEK]:  # ft.SubType.K_15M, ft.SubType.K_1M
            ret_code, ret_data = quote_ctx.get_cur_kline(code, 1000, ktype)
            if ret_code == ft.RET_ERROR:
                print(code, ktype, ret_data)
                exit()
            kline_table = ret_data
            print("%s KLINE %s" % (code, ktype))
            kline_table['rsi13'] = talib.RSI(kline_table['close'], RSI_NUM)
            b = kline_table.iloc[-1]
            # b.at["note"] = b.code + ' ' + str(b.close) + ': rsi13(' + ktype + ') ' + str(round(b.rsi13))
            b.at["note"] = '{:<8} {:<9.2f} {:<9.2f}'.format(b.code, b.rsi13, b.close)

            # print(kline_table)
            # print("\n\n")
            resultList.append(b)

    output_message = 'RSI update: \n{:<6} {:<11} {:<4}\n'.format('Code', 'rsi' + str(RSI_NUM) + str(ktype[2:]), 'close')
    for i in resultList:
        output_message += i.note + '\n'

    print(output_message)
    # CkTelegram().send_message_group(output_message)
    CkTelegram().send_message_ck(output_message)


if __name__ == "__main__":
    quote_ctx = ft.OpenQuoteContext()
    _example_cur_kline(quote_ctx)

    # quote_ctx.close()