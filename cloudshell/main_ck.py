# T : telegram
class ckTelegram:
    import telegram

    T_TOKEN = "456425019:AAGPvI1Gi4LdD9zaOz9l9E0S2BuYefcJpDE"
    T_CHATID_CK = "212470449"
    T_CHATID_GROUP = "-297241281"

    def __init__(s):
        s.bot = s.telegram.Bot(token=s.T_TOKEN)

    def send_message(s, id, message):
        s.bot.send_message(id, message)

    def send_message_ck(s, message):
        s.send_message(s.T_CHATID_CK, message)

    def send_message_group(s, message):
        s.send_message(s.T_CHATID_GROUP, message)


import futu as ft
import talib

RSI_NUM = 13
# subscribe Kline

stock_code_list = [
    "US.AMZN", "US.MSFT", "US.SPXL", "US.HACK", "US.NVDA", "US.ADBE",
    "US.MA", "US.COST", "US.UNH", "US.CRM", "US.AAPL"
]
sub_type_list = [
    ft.SubType.K_15M, ft.SubType.K_30M, ft.SubType.K_DAY, ft.SubType.RT_DATA, ft.SubType.TICKER
]
loop_type_list = [
    ft.SubType.K_30M, ft.SubType.K_DAY
]


def _example_cur_kline(quote_ctx):
    ret_status, ret_data = quote_ctx.subscribe(stock_code_list, sub_type_list)
    if ret_status != ft.RET_OK:
        print(ret_data)
        exit()

    ret_status, ret_data = quote_ctx.query_subscription()
    if ret_status == ft.RET_ERROR:
        print(ret_data)
        exit()
    print(ret_data)

    result_dict = {}

    for stock_code in stock_code_list:
        for ktype in loop_type_list:  # ft.SubType.K_15M, ft.SubType.K_1M

            ret_code, ret_data = quote_ctx.get_cur_kline(stock_code, 300, ktype)
            if ret_code == ft.RET_ERROR:
                print("failure: ", stock_code, ktype)
                exit()
            if ret_data.empty:
                continue
            print("%s KLINE %s success" % (stock_code, ktype))

            # code                         US.AMZN
            # time_key         2018-09-14 16:00:00
            # open                         1968.42
            # close                        1970.19
            # high                          1971.5
            # low                          1967.01
            # volume                        554863
            # turnover                 1.09291e+09
            # pe_ratio                           0
            # turnover_rate                      0
            # last_close                   1968.28

            if (stock_code not in result_dict):
                result_dict[stock_code] = {}
                last_row = ret_data.iloc[-1]
                result_dict[stock_code]["code"] = last_row["code"]
                result_dict[stock_code]["close"] = quote_ctx.get_rt_ticker(stock_code, 1)[1]["price"][0]

            result_dict[stock_code][ktype[2:] + "_rsi"] = talib.RSI(ret_data['close'], RSI_NUM).iloc[-1]

    return result_dict


def print_result_dict(result_dict):
    if not result_dict:
        return
    import pandas as pd
    pd.options.display.float_format = "{:.2f}".format
    df = pd.DataFrame.from_dict(result_dict, orient='index')
    output_message = df.to_string(index=False)
    print(output_message)

    # ckTelegram().send_message_group(output_message)
    ckTelegram().send_message_ck(output_message)


if __name__ == "__main__":
    quote_ctx = ft.OpenQuoteContext()
    result_dict = _example_cur_kline(quote_ctx)
    print_result_dict(result_dict)

    quote_ctx.close()

    # quote_ctx.get_rt_ticker('HK.00700', 10)
