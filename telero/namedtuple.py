from .telepot.namedtuple import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
    ReplyKeyboardRemove,
    ForceReply,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedGif,
    InlineQueryResultCachedMpeg4Gif,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InlineQueryResultContact,
    InlineQueryResultGame,
    InlineQueryResultDocument,
    InlineQueryResultGif,
    InlineQueryResultLocation,
    InlineQueryResultMpeg4Gif,
    InlineQueryResultPhoto,
    InlineQueryResultVenue,
    InlineQueryResultVideo,
    InlineQueryResultVoice,
    InputTextMessageContent,
    InputLocationMessageContent,
    InputVenueMessageContent,
    InputContactMessageContent,
    LabeledPrice,
    ShippingOption
)


def Keyboard(_):
    return ReplyKeyboardMarkup(keyboard=_)


def InlineKeyboard(_):
    return InlineKeyboardMarkup(inline_keyboard=_)


def Button(text, **kwargs):
    return KeyboardButton(text=text, **kwargs)


def InlineButton(text, **kwargs):
    return InlineKeyboardButton(text=text, **kwargs)


def KeyboardRemove(selective=False):
    return ReplyKeyboardRemove(selective=selective)
