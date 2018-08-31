# T : telegram
class CkTelegram:
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