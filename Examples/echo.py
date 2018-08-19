from TelegramApiClient import *

Api_Token = "123456789:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
client = Client(Api_Token)
bot = client.Bot()

@client.message(Filter.text)
def MessageHandler(message):
    message.reply(message.text)

client.run()
