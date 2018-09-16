import futuquant as ft
import talib

RSI_NUM = 13
# subscribe Kline

stock_code_list = ["US.AMZN",
                   "US.MSFT",
                   "US.SPXL",
                   "US.HACK",
                   "US.NVDA",
                   "US.ADBE",
                   "US.MA",
                   "US.COST",
                   "US.UNH",
                   "US.CRM"
                   ]
sub_type_list = [ft.SubType.K_15M,
                 ft.SubType.K_30M,
                 ft.SubType.K_DAY]

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

    resultList = []

    for code in stock_code_list:
        for ktype in sub_type_list:  # ft.SubType.K_15M, ft.SubType.K_1M
            ret_code, ret_data = quote_ctx.get_cur_kline(code, 1000, ktype)
            if ret_code == ft.RET_ERROR:
                print(code, ktype, ret_data)
                exit()
            kline_table = ret_data
            print("%s KLINE %s" % (code, ktype))
            kline_table['rsi13'] = talib.RSI(kline_table['close'], RSI_NUM)
            b = kline_table.iloc[-1]
            b.at["note"] = '{:<8} {:<9.2f} {:<5} {:<9.2f} '.format(b.code, b.close, str(ktype[2:]), b.rsi13)

            # print(kline_table)
            # print("\n\n")
            resultList.append(b)

    outputMessage = 'RSI update: \n{:<8} {:<9} {:<5} {:<9}\n'.format('Code', 'close', 'ktype', 'rsi')
    for i in resultList:
        outputMessage += i.note + '\n'
        
    print(""+outputMessage)
    # ckTelegram().send_message_group(outputMessage)
    ckTelegram().send_message_ck(outputMessage)

if __name__ == "__main__":
    quote_ctx = ft.OpenQuoteContext()
    _example_cur_kline(quote_ctx)
    
    quote_ctx.close()