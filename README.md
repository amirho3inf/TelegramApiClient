## Write your Telegram Bot faster and easier! (based on [telepot](https://github.com/nickoala/telepot))

# Installation ⚙️
```
pip3 install telero
```

# Example 💡

```
from telero import Client, Filters

TOKEN = "670453257:AAGrvQjihO21Dibc5F3HOTXFI6mFuM16S9g"
client = Client(TOKEN)

@client.message(Filters.private & Filters.text)
def handle(bot, message):
    # echo anything in private chat
    message.reply(message.text)

client.run()

```


# Guide 📙
not ready yet :(