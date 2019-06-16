import re


class FilterBase(object):
    def __call__(self, message):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(FilterBase):
    def __init__(self, f):
        self.f = f

    def __call__(self, msg):
        return not self.f(msg)


class AndFilter(FilterBase):
    def __init__(self, f, other):
        self.f = f
        self.other = other

    def __call__(self, msg):
        return self.f(msg) and self.other(msg)


class OrFilter(FilterBase):
    def __init__(self, f, other):
        self.f = f
        self.other = other

    def __call__(self, msg):
        return self.f(msg) or self.other(msg)


def _build(n, f):
    return type(n, (FilterBase,), {
        "__call__": lambda self, *args, **kwargs: f(*args, **kwargs)
    })()


class Filters(object):

    text = _build('text', lambda msg: bool(msg.message.text or msg.text))

    photo = _build('photo', lambda msg: bool(msg.message.photo or msg.photo))

    video = _build('video', lambda msg: bool(msg.message.video or msg.video))

    voice = _build('voice', lambda msg: bool(msg.message.voice or msg.voice))

    audio = _build('audio', lambda msg: bool(msg.message.audio or msg.audio))

    document = _build('document', lambda msg: bool(
        msg.message.document or msg.document))

    sticker = _build('sticker', lambda msg: bool(
        msg.message.sticker or msg.sticker))

    video_note = _build('video_note', lambda msg: bool(
        msg.message.video_note or msg.video_note))

    audio = _build('audio', lambda msg: bool(msg.message.audio or msg.audio))

    supergroup = _build(
        'supergroup', lambda msg: (msg.chat and msg.chat.type == 'supergroup') or (
            msg.message and msg.message.chat.type == 'supergroup')
    )

    group = _build(
        'group', lambda msg: (msg.chat and msg.chat.type == 'group') or (
            msg.message and msg.message.chat.type == 'group')
    )

    private = _build(
        'private', lambda msg: (msg.chat and msg.chat.type == 'private') or (
            msg.message and msg.message.chat.type == 'private')
    )

    channel = _build(
        'channel', lambda msg: (msg.chat and msg.chat.type == 'channel') or (
            msg.message and msg.message.chat.type == 'channel')
    )

    reply = _build('reply', lambda msg: bool(
        msg.reply_to_message or (msg.message and msg.message.reply_to_message)))

    forwarded = _build('forwarded', lambda msg: bool(msg.forward_date))

    caption = _build('caption', lambda msg: bool(
        msg.caption or (msg.message and msg.message.caption)))

    edited = _build('edited', lambda msg: bool(msg.edit_date))

    contact = _build('contact', lambda msg: bool(msg.contact))

    location = _build('location', lambda msg: bool(msg.location))

    new_chat_members = _build(
        'new_chat_members', lambda msg: bool(msg.new_chat_members))

    left_chat_member = _build(
        'left_chat_member', lambda msg: bool(msg.left_chat_member))

    new_chat_title = _build(
        'new_chat_title', lambda msg: bool(msg.new_chat_title))

    new_chat_photo = _build(
        'new_chat_photo', lambda msg: bool(msg.new_chat_photo))

    delete_chat_photo = _build(
        'delete_chat_photo', lambda msg: bool(msg.delete_chat_photo))

    pinned_message = _build(
        'pinned_message', lambda msg: bool(msg.pinned_message))

    @staticmethod
    def command(pattern):
        _patt = re.compile(pattern, flags=re.MULTILINE | re.DOTALL)

        def _check(msg):
            matches = _patt.findall(msg.text)
            if not matches:
                return False
            msg.update({"matches": matches})
            return True

        return _build('command', _check)

    @staticmethod
    def chat(chat_id):

        def _check(msg):
            if msg.chat:
                _chat_id_ = msg.chat.id
            elif msg.message:
                _chat_id_ = msg.message.chat.id

            return (_chat_id_ == chat_id)

        if isinstance(chat_id, int):
            return _build('chat', _check)

        if isinstance(chat_id, list):
            return _build('chat', lambda msg: True in [_check(msg) for ch in chat_id])

    @staticmethod
    def username(usr):
        if isinstance(usr, str):
            usr = usr.strip("@").lower()
        if isinstance(usr, list):
            for i, u in enumerate(usr):
                usr[i] = u.strip("@").lower()

        def _check(msg):
            _usrn = (msg.chat.username if msg.chat else None) or (
                msg.message.chat.username if msg.message else None)
            if not _usrn:
                return
            _usrn = _usrn.lower()

            if isinstance(usr, str):
                return _usrn == usr
            if isinstance(usr, list):
                for u in usr:
                    if _usrn == u:
                        return True

        return _build('username', _check)
