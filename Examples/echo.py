from TelegramApiClient import *

Api_Token = "123456789:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
client = Client(Api_Token)
bot = client.Bot()

@client.message()
def MessageHandler(message):
    message.reply(message.text)

client.run()
