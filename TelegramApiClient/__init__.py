import re
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from telepot.loop import MessageLoop
import threading
import json

class Filter:
    def __call__(self, message):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)

class InvertFilter(Filter):
    def __init__(self, func):
        self.func = func

    def __call__(self, message):
        return not self.func(message)

class AndFilter(Filter):
    def __init__(self, func, other):
        self.func = func
        self.other = other

    def __call__(self, message):
        return self.func(message) and self.other(message)

class OrFilter(Filter):
    def __init__(self, func, other):
        self.func = func
        self.other = other

    def __call__(self, message):
        return self.func(message) or self.other(message)

def BUILD(name, func):
    return type(name, (Filter,), {"__call__": func})()

class Filters:
    text = BUILD('text', lambda _, message: ("text" in message['message']) if ("message" in message) else ("text" in message))

    photo = BUILD('photo', lambda _, message: ("photo" in message['message']) if ("message" in message) else ("photo" in message))

    video = BUILD('video', lambda _, message: ("video" in message['message']) if ("message" in message) else ("video" in message))

    voice = BUILD('voice', lambda _, message: ("voice" in message['message']) if ("message" in message) else ("voice" in message))

    audio = BUILD('audio', lambda _, message: ("audio" in message['message']) if ("message" in message) else ("audio" in message))

    document = BUILD('document', lambda _, message: ("document" in message['message']) if ("message" in message) else ("document" in message))

    sticker = BUILD('sticker', lambda _, message: ("sticker" in message['message']) if ("message" in message) else ("sticker" in message))

    video_note = BUILD('video_note', lambda _, message: ("video_note" in message['message']) if ("message" in message) else ("video_note" in message))

    supergroup = BUILD('supergroup', lambda _, message: (message['chat']['type'] == 'supergroup'))

    private = BUILD('private', lambda _, message: (message['chat']['type'] == 'private'))

    group = BUILD('group', lambda _, message: (message['chat']['type'] == 'group'))

    channel = BUILD('channel', lambda _, message: (message['chat']['type'] == 'channel'))

    reply = BUILD('reply', lambda _, message: ('reply_to_message' in message))

    forwarded = BUILD('forwarded', lambda _, message: ('forward_date' in message))

    caption = BUILD('caption', lambda _, message: ('caption' in message))

    edited = BUILD('edited', lambda _, message: ('edit_date' in message))

    contact = BUILD('contact', lambda _, message: ('contact' in message))

    location = BUILD('location', lambda _, message: ('location' in message))

    new_chat_members = BUILD('new_chat_members', lambda _, message: ('new_chat_members' in message))

    left_chat_member = BUILD('left_chat_member', lambda _, message: ('left_chat_member' in message))

    new_chat_title = BUILD('new_chat_title', lambda _, message: ('new_chat_title' in message))

    new_chat_photo = BUILD('new_chat_photo', lambda _, message: ('new_chat_photo' in message))

    delete_chat_photo = BUILD('delete_chat_photo', lambda _, message: ('delete_chat_photo' in message))

    pinned_message = BUILD('pinned_message', lambda _, message: ('pinned_message' in message))

    def command(pattern):
        regex = re.compile(pattern, flags=re.MULTILINE | re.DOTALL)
        return BUILD('command', (lambda _, message: regex.match(message['text']) if ('text' in message) else False))

    def chat_id(ChatFilter):
        if type(ChatFilter) is list:
            return BUILD('chat_id', (lambda _, message: (True in [(message['chat']['id']==chat) for chat in ChatFilter])))
        elif type(ChatFilter) is int:
            return BUILD('chat_id', lambda _, message: (message['chat']['id']==ChatFilter))

    def chat_name(NameFilter):
        def Check(_, message):
            NameFilter = NameFilter.lower()
            chat_name = message['chat']['title'].lower() if ('title' in message['chat']) else ''
            lastName = ' '+message['chat']['last_name'].lower() if ('last_name' in message['chat']) else ''
            chat_name = message['chat']['first_name'].lower()+lastName if 'first_name' in message['chat'] else ''
            if type(NameFilter) is list:
                for name in NameFilter:
                    if name == chat_name: return True
            elif type(NameFilter) is str:
                return NameFilter==chat_name
        return BUILD('chat_name', Check)

    def chat_username(UsernameFilter):
        def Check(_, message):
            username = message['chat']['username'].lower() if 'username' in message['chat'] else ''
            if type(UsernameFilter) is list:
                    for Username in UsernameFilter:
                        if username == Username.lower().replace('@', ''): return True
            elif type(UsernameFilter) is str:
                return username==UsernameFilter.lower().replace('@', '')
        return BUILD('chat_username', Check)

class MessageObject:
    def __init__(self, bot, update):
        self.update = update
        try: self.text = update['text']
        except: self.text = ''
        try: self.sender = update['from']['id']
        except: self.sender = None
        self.chat = update['chat']['id']
        self.bot = bot

    def __str__(self):
        return json.dumps(self.update, indent=4, sort_keys=True)

    def __getitem__(self, item):
        return self.update[item]

    def __contains__(self, item):
        try: return (item in self.update)
        except: pass

    def __getattr__(self, item):
        try: return self.update[item]
        except: pass

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
    def __init__(self, token, proxy=None):
        self.token = token
        self.bot = telepot.Bot(token)
        if proxy:
            try: username = proxy['username']; password = proxy['password']
            except: username = None; password = None
            if username and password : basic_auth = (proxy['username'], proxy['password'],)
            else: basic_auth = None
            telepot.api.set_proxy(proxy['url'], basic_auth=basic_auth)
        self._callback_query_handlers = []
        self._inline_query_handlers = []
        self._message_handlers = []
    def message(self, filter=lambda message: True):
        def inner(func):
            self._message_handlers.append(lambda message: func(message) if filter(message) else None)
        return inner
    def callback_query(self, filter=lambda message: True):
        def inner(func):
            self._callback_query_handlers.append(lambda message: func(message) if filter(message) else None)
        return inner
    def inline_query(self):
        def inner(func):
            self._inline_query_handlers.append(func)
        return inner
    def Bot(self):
        return self.bot
    def run(self):
        def MessagesProcessor(update):
            update['type'] = "message"
            for func in self._message_handlers: threading.Thread(target=func, args=(MessageObject(self.bot, update),)).start()
        def CallbackQueriesProcessor(update):
            update['type'] = "callback_query"
            update['text'] = update['data']
            update["chat"] = update["message"]["chat"]
            update["message_id"] = update["message"]["message_id"]
            for func in self._callback_query_handlers: threading.Thread(target=func, args=(MessageObject(self.bot, update),)).start()
        def InlineQueriesProcessor(update):
            update['type'] = "inline_query"
            update['text'] = update['query']
            update['chat'] = update['from']
            update['message_id'] = 0
            for func in self._inline_query_handlers: threading.Thread(target=func, args=(MessageObject(self.bot, update),)).start()
        MessageLoop(self.bot, {
        'chat': MessagesProcessor,
        'callback_query': CallbackQueriesProcessor,
        'inline_query': InlineQueriesProcessor,
        }).run_as_thread()
        print("TelegramApiClient runned as @{}".format(self.bot.getMe()['username']))
        while 1:
            time.sleep(10)
RemoveKeyboard = ReplyKeyboardRemove
Keyboard = lambda data, resize_keyboard=True: ReplyKeyboardMarkup(keyboard=data, resize_keyboard=resize_keyboard)
InlineKeyboard = lambda data: InlineKeyboardMarkup(inline_keyboard=data)
