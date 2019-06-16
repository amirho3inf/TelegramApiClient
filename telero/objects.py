import json
from .telepot import Bot as bot_base


class Employee(dict):

    def __getattr__(self, attr):
        v = self.get(attr)

        if not v:
            return

        if isinstance(v, dict):
            return Employee(v)

        if isinstance(v, list):
            __l = []
            for it in v:

                if isinstance(it, (list, dict)):
                    __l.append(Employee(it))
                    continue

                __l.append(it)

            return __l

        return v

    def __str__(self):
        return json.dumps(self, indent=2)


class UpdateMethods(object):

    def reply(self, text='', *args, **kwargs):
        dont_reply = kwargs.pop("dont_reply", None)

        if 'photo' in kwargs:
            photo = kwargs.pop("photo")
            return __bot__.sendPhoto(self.chat.id,
                                     photo, *args, caption=text,
                                     reply_to_message_id=0 if dont_reply else self.message_id,
                                     **kwargs)

        if 'document' in kwargs:
            document = kwargs.pop("document")
            return __bot__.sendDocument(self.chat.id,
                                        document, *args, caption=text,
                                        reply_to_message_id=0 if dont_reply else self.message_id,
                                        **kwargs)
        if 'video' in kwargs:
            video = kwargs.pop("video")
            return __bot__.sendVideo(self.chat.id,
                                     video, *args, caption=text,
                                     reply_to_message_id=0 if dont_reply else self.message_id,
                                     **kwargs)

        if 'voice' in kwargs:
            voice = kwargs.pop("voice")
            return __bot__.sendVoice(self.chat.id,
                                     voice, *args, caption=text,
                                     reply_to_message_id=0 if dont_reply else self.message_id,
                                     **kwargs)

        if 'audio' in kwargs:
            audio = kwargs.pop("audio")
            return __bot__.sendAudio(self.chat.id,
                                     audio, *args, caption=text,
                                     reply_to_message_id=0 if dont_reply else self.message_id,
                                     **kwargs)

        if 'video_note' in kwargs:
            video_note = kwargs.pop("video_note")
            return __bot__.sendVideoVote(self.chat.id,
                                         video_note, *args, caption=text,
                                         reply_to_message_id=0 if dont_reply else self.message_id,
                                         **kwargs)

        if 'sticker' in kwargs:
            sticker = kwargs.pop("sticker")
            return __bot__.sendSticker(self.chat.id,
                                       sticker, *args,
                                       reply_to_message_id=0 if dont_reply else self.message_id,
                                       **kwargs)

        return __bot__.sendMessage(self.chat.id,
                                   text, *args,
                                   reply_to_message_id=0 if dont_reply else self.message_id,
                                   **kwargs)

    def respond(self, *args, **kwargs):
        self.reply(*args, dont_reply=True, **kwargs)

    def forward(self, chat_id, *args, **kwargs):
        return __bot__.forwardMessage(chat_id,
                                      from_chat_id=self.chat.id,
                                      message_id=self.message_id,
                                      *args, **kwargs)

    def answer(self, text, alert=False):
        return __bot__.answerCallbackQuery(self.id, text, alert)

    def answer_inline(self, results, *args, **kwargs):
        return __bot__.answerInlineQuery(self.id, results, *args, **kwargs)

    def delete(self):
        return __bot__.deleteMessage((self.chat.id, self.message_id))

    def edit(self, text='', *args, **kwargs):
        msg = (self.message or self)

        if not text and kwargs.get("reply_markup"):
            return __bot__.editMessageReplyMarkup((self.chat.id, self.message_id),
                                                  kwargs.get("reply_markup"))

        if 'text' in msg:
            return __bot__.editMessageText((self.chat.id, self.message_id),
                                           text, *args, **kwargs)

        if 'caption' in msg:
            return __bot__.editMessageCaption((self.chat.id, self.message_id),
                                              text, *args, **kwargs)


class TelegramUpdate(UpdateMethods, Employee):

    def __init__(self, update):
        super(TelegramUpdate, self).__init__(update)

    def __repr__(self):
        return "TelegramUpdate(date={})".format(self.date)


class Bot(bot_base):
    def __init__(self, token):
        super().__init__(token)
        global __bot__
        __bot__ = self

    def __getattribute__(self, attr):
        _ = getattr(super(), attr, None) or self.__dict__.get(attr, None)

        if not _:
            raise AttributeError(attr + " method does not exist")

        if not callable(_):
            return _

        def __(*args, **kwargs):
            r = _(*args, **kwargs)
            return TelegramUpdate(r) if isinstance(r, dict) else r

        return __
