from TelegramApiClient import Client, Filters

Api_Token = "123456789:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
client = Client(Api_Token)
bot = client.Bot()

@client.message(Filters.text)
def MessageHandler(message):
    message.reply(message.text)

client.run()
