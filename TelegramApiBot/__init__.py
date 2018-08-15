import re
import telepot
import telepot.aio
from telepot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
import asyncio
import threading
class Filters:
    def text(func):
        def inner(client, update):
            if "message" in update:
                if "text" in update['message']:
                    func(client, update)
            elif "text" in update:
                func(client, update)
        return inner
    def photo(func):
        def inner(client, update):
            if "message" in update:
                if "photo" in update['message']:
                    func(client, update)
            elif "photo" in update:
                func(client, update)
        return inner
    def video(func):
        def inner(client, update):
            if "message" in update:
                if "video" in update['message']:
                    func(client, update)
            elif "video" in update:
                func(client, update)
        return inner
    def voice(func):
        def inner(client, update):
            if "message" in update:
                if "voice" in update['message']:
                    func(client, update)
            elif "voice" in update:
                func(client, update)
        return inner
    def audio(func):
        def inner(client, update):
            if "message" in update:
                if "audio" in update['message']:
                    func(client, update)
            elif "audio" in update:
                func(client, update)
        return inner
    def document(func):
        def inner(client, update):
            if "message" in update:
                if "document" in update['message']:
                    func(client, update)
            elif "document" in update:
                func(client, update)
        return inner
    def sticker(func):
        def inner(client, update):
            if "message" in update:
                if "sticker" in update['message']:
                    func(client, update)
            elif "sticker" in update:
                func(client, update)
        return inner
    def video_note(func):
        def inner(client, update):
            if "message" in update:
                if "video_note" in update['message']:
                    func(client, update)
            elif "video_note" in update:
                func(client, update)
        return inner
    def command(pattern):
        def inner(func):
            def inner2(client, update):
                regex = re.compile(pattern, flags=re.MULTILINE | re.DOTALL)
                if "text" in update and regex.match(update['text']):
                    func(client, update)
            return inner2
        return inner
    def group(func):
        def inner(client, update):
            if update['chat']['type'] == 'group':
                func(client, update)
        return inner
    def supergroup(func):
        def inner(client, update):
            if update['chat']['type'] == 'supergroup':
                func(client, update)
        return inner
    def private(func):
        def inner(client, update):
            if update['chat']['type'] == 'private':
                func(client, update)
        return inner
    def channel(func):
        def inner(client, update):
            if update['chat']['type'] == 'channel':
                func(client, update)
        return inner
    def chat_id(chat_id):
        def inner(func):
            def inner2(client, update):
                if type(chat_id) is list:
                    for id in chat_id:
                        if update['chat']['id'] == id:
                            func(client, update)
                elif type(chat_id) is int:
                    if update['chat']['id'] == chat_id:
                        func(client, update)
            return inner2
        return inner
    def chat_name(filter_name):
        def inner(func):
            def inner2(client, update):
                if "title" in update['chat']:
                    chat_name = update['chat']['title']
                elif "first_name" in update['chat']:
                    chat_name = update['chat']["first_name"]
                    if "last_name" in update['chat']:
                        chat_name += " " + update['chat']['last_name']
                if type(filter_name) is list:
                    for name in filter_name:
                        if str(name) == chat_name:
                            func(client, update)
                elif type(filter_name) is str:
                    if filter_name == chat_name:
                        func(client, update)
            return inner2
        return inner
    def chat_username(filter_username):
        def inner(func):
            def inner2(client, update):
                if 'username' in update['chat']:
                    username = update['chat']['username'].lower()
                else:
                    username = ''
                if type(filter_username) is list:
                    for chat_username in filter_username:
                        chat_username = chat_username.replace("@", "")
                        if str(chat_username).lower() == username:
                            func(client, update)
                elif type(filter_username) is str:
                    filter_username = filter_username.replace("@", "")
                    if filter_username.lower() == username:
                        func(client, update)
            return inner2
        return inner
class handlerObject:
    def __init__(self, func, filter):
        self.filter = filter
        self.func = func
    def process(self, client, message):
        @self.filter
        def subprocess(client, message):
            self.func(client, message)
        subprocess(client, message)
class SubClient:
    def __init__(self, bot, update):
        self.update = update
        self.message_id = update['message_id']
        self.message_type = update['type']
        self.text = ''
        self.callback_id = None
        self.inline_id = None
        try: self.text = update['text']
        except: pass
        if self.message_type == "callback_query": self.callback_id = update['id']
        if self.message_type == "inline_query": self.inline_id = update['id']
        try: self.sender = update['from']['id']
        except: self.sender = None
        self.chat = update['chat']['id']
        self.bot = bot
    def reply(self, text=None, photo=None, sticker=None, document=None, voice=None, audio=None, video=None, video_note=None, duration=None, length=None, parse_mode=None, disable_web_page_preview=None, disable_notification=None, reply_markup=None):
        if photo:
            return self.bot.sendPhoto(self.update['chat']['id'], photo, caption=text, reply_to_message_id=self.update['message_id'], parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif document:
            return self.bot.sendDocument(self.update['chat']['id'], document, caption=text, reply_to_message_id=self.update['message_id'], parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif video:
            return self.bot.sendVideo(self.update['chat']['id'], video, caption=text, reply_to_message_id=self.update['message_id'], parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif voice:
            return self.bot.sendVoice(self.update['chat']['id'], voice, caption=text, reply_to_message_id=self.update['message_id'], parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif audio:
            return self.bot.sendAudio(self.update['chat']['id'], audio, caption=text, reply_to_message_id=self.update['message_id'], parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif video_note:
            return self.bot.sendVideoNote(self.update['chat']['id'], video_note, duration=None, length=None, reply_to_message_id=self.update['message_id'], disable_notification=disable_notification, reply_markup=reply_markup)
        elif sticker:
            return self.bot.sendSticker(self.update['chat']['id'], sticker, reply_to_message_id=self.update['message_id'], disable_notification=disable_notification, reply_markup=reply_markup)
        elif text:
            return self.bot.sendMessage(self.update['chat']['id'], text, reply_to_message_id=self.update['message_id'], parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview, disable_notification=disable_notification, reply_markup=reply_markup)
    def respond(self, text=None, photo=None, sticker=None, document=None, reply_to_message_id=None, voice=None, audio=None, video=None, video_note=None, duration=None, length=None, parse_mode=None, disable_web_page_preview=None, disable_notification=None, reply_markup=None):
        if photo:
            return self.bot.sendPhoto(self.update['chat']['id'], photo, caption=text, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif document:
            return self.bot.sendDocument(self.update['chat']['id'], document, caption=text, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif video:
            return self.bot.sendVideo(self.update['chat']['id'], video, caption=text, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif voice:
            return self.bot.sendVoice(self.update['chat']['id'], voice, caption=text, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif audio:
            return self.bot.sendAudio(self.update['chat']['id'], audio, caption=text, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode, disable_notification=disable_notification, reply_markup=reply_markup)
        elif video_note:
            return self.bot.sendVideoNote(self.update['chat']['id'], video_note, duration=None, length=None, reply_to_message_id=reply_to_message_id, disable_notification=disable_notification, reply_markup=reply_markup)
        elif sticker:
            return self.bot.sendSticker(self.update['chat']['id'], sticker, reply_to_message_id=reply_to_message_id, disable_notification=disable_notification, reply_markup=reply_markup)
        elif text:
            return self.bot.sendMessage(self.update['chat']['id'], text, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview, disable_notification=disable_notification, reply_markup=reply_markup)
    def answer(self, text, alert=None):
        if self.update['type'] == "callback_query":
            return self.bot.answerCallbackQuery(self.update['id'], text, show_alert=alert)
    def forward(self, chat_id, disable_notification=None):
        return self.bot.forwardMessage(chat_id, from_chat_id=self.update['chat']['id'], message_id=self.update['message_id'], disable_notification=disable_notification)
    def delete(self):
        return self.bot.deleteMessage((self.update['chat']['id'], self.update['message_id'],))
    def edit(self, text, parse_mode=None, disable_web_page_preview=None, reply_markup=None):
        if "text" in self.update['message']:
            return self.bot.editMessageText((self.update['chat']['id'], self.update['message_id'],), text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview, reply_markup=reply_markup)
        elif "caption" in self.update['message']:
            return self.bot.editMessageCaption((self.update['chat']['id'], self.update['message_id'],), text, parse_mode=parse_mode, reply_markup=reply_markup)
    def edit_reply_markup(self, reply_markup):
        return self.bot.editMessageReplyMarkup((self.update['chat']['id'], self.update['message_id'],), reply_markup=reply_markup)
class Client:
    def __init__(self, token):
        self.token = token
        self.bot = telepot.Bot(token)
        self._callback_query_handlers = []
        self._inline_query_handlers = []
        self._message_handlers = []
        self._edited_message_handlers = []
    def message(self, filter=lambda func: (lambda client, update: func(client, update))):
        def inner(func):
            self._message_handlers.append(handlerObject(func, filter).process)
        return inner
    def edited_message(self, filter=lambda func: (lambda client, update: func(client, update))):
        def inner(func):
            self._edited_message_handlers.append(handlerObject(func, filter).process)
        return inner
    def callback_query(self, filter=lambda func: (lambda client, update: func(client, update))):
        def inner(func):
            self._callback_query_handlers.append(handlerObject(func, filter).process)
        return inner
    def inline_query(self):
        def inner(func):
            self._inline_query_handlers.append(func)
        return inner
    def Bot(self):
        return self.bot
    def run(self):
        @asyncio.coroutine
        def updates_processor(update):
            if "data" in update:
                update['type'] = "callback_query"
                update['text'] = update['data']
                update["chat"] = update["message"]["chat"]
                update["message_id"] = update["message"]["message_id"]
                for func in self._callback_query_handlers: threading.Thread(target=func, args=(SubClient(self.bot, update), update,)).start()
            elif "query" in update:
                update['type'] = "inline_query"
                update['text'] = update['query']
                update['chat'] = update['from']
                update['message_id'] = None
                for func in self._inline_query_handlers: threading.Thread(target=func, args=(SubClient(self.bot, update), update,)).start()
            else:
                update['type'] = "message"
                if "edit_date" in update:
                    for func in self._edited_message_handlers: threading.Thread(target=func, args=(SubClient(self.bot, update), update)).start()
                else:
                    for func in self._message_handlers: threading.Thread(target=func, args=(SubClient(self.bot, update), update)).start()
        bot = telepot.aio.Bot(self.token)
        answerer = telepot.aio.helper.Answerer(bot)
        loop = asyncio.get_event_loop()
        loop.create_task(bot.message_loop({'chat': updates_processor, 'callback_query': updates_processor, 'inline_query': updates_processor, }))
        print("TelegramApiClient runned as @{}".format(self.bot.getMe()['username']))
        loop.run_forever()
RemoveKeyboard = ReplyKeyboardRemove
Keyboard = lambda data, resize_keyboard=True: ReplyKeyboardMarkup(keyboard=data, resize_keyboard=resize_keyboard)
InlineKeyboard = lambda data: InlineKeyboardMarkup(inline_keyboard=data)
