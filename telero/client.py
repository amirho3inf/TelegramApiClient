import time
from .telepot import api
from .telepot.loop import MessageLoop
from .objects import TelegramUpdate, Bot


class Client(object):

    def __init__(self, token, proxy=None):
        self._token = token
        self._bot = Bot(token)
        self._callback_query_handlers = []
        self._inline_query_handlers = []
        self._message_handlers = []

        if isinstance(proxy, dict):
            url = proxy.get("url")
            username = proxy.get("username")
            password = proxy.get("password")

            userpass = None
            if username and password:
                userpass = (username, password)

            if url:
                api.set_proxy(url, userpass)

    def Bot(self):
        return self._bot

    def message(self, _filter=None):

        def inner(func):
            self._message_handlers.append(
                (func, _filter)
            )

        return inner

    def callback_query(self, _filter=None):

        def inner(func):
            self._callback_query_handlers.append(
                (func, _filter)
            )

        return inner

    def inline_query(self, _filter=None):

        def inner(func):
            self._inline_query_handlers.append(
                (func, _filter)
            )

        return inner

    def _messages_processor(self, msg):
        msg = TelegramUpdate(msg)
        for func, _filter in self._message_handlers:
            if not _filter or _filter(msg):
                func(self._bot, msg)

    def _callback_queries_processor(self, msg):
        msg = TelegramUpdate(msg)
        for func, _filter in self._callback_query_handlers:
            if not _filter or _filter(msg):
                func(self._bot, msg)

    def _inline_queries_processor(self, msg):
        msg = TelegramUpdate(msg)
        for func, _filter in self._inline_query_handlers:
            if not _filter or _filter(msg):
                func(self._bot, msg)

    def run(self):
        MessageLoop(self._bot, {
            'chat': self._messages_processor,
            'callback_query': self._callback_queries_processor,
            'inline_query': self._inline_queries_processor,
        }).run_as_thread()

        print("Telero runned as @{}".format(
            self._bot.getMe().username))

        while 1:
            time.sleep(10)
