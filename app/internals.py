from datetime import date

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from Localization import localize
from typing import Union
import datetime
import dateparser


def get_lang(update: Update):
    try:
        return update.effective_message.from_user.language_code
    except AttributeError:
        pass

    try:
        return update.callback_query.from_user.language_code
    except AttributeError:
        pass

    return "en"


def get_raw_commands(lang="fr"):
    commands = []
    for command in ["commands", "search", "interests", "phone", "location", "contact", "stop"]:
        commands += [
            ("/%s" % command, "%s" % localize("command %s" % command, lang)),
        ]
    return commands


def get_commands(lang="fr", exclude=None):
    button_list = []
    for command, desc in get_raw_commands(lang):
        if exclude is not None and command in exclude:
            continue
        button_list += [[
            KeyboardButton("%s - %s" % (command, desc)),
        ]]
    button_list += [[
        KeyboardButton(localize("exit menu", lang))
    ]]

    reply = ReplyKeyboardMarkup(button_list, one_time_keyboard=True)

    return reply


def get_message_text(update: Update):
    if update.message is not None:
        return update.message.text

    if update.callback_query is not None:
        return update.callback_query.data


def get_message(update: Update):
    if update.message is not None:
        return update.message

    if update.callback_query is not None:
        return update.callback_query.message


def edit_message(message, update: Update, context: CallbackContext, reply_markup: InlineKeyboardMarkup = None,
                 local: bool = True):
    if local:
        message = localize(message, get_lang(update))

    if update.message is not None:
        context.bot.edit_message_text(text=message,
                                      chat_id=update.message.chat_id,
                                      message_id=update.message.message_id,
                                      reply_markup=reply_markup)

    if update.callback_query is not None:
        context.bot.edit_message_text(text=message,
                                      chat_id=update.callback_query.message.chat.id,
                                      message_id=update.callback_query.message.message_id,
                                      inline_message_id=update.callback_query.inline_message_id,
                                      reply_markup=reply_markup)


def send_message(message, update: Update,
                 context: CallbackContext,
                 reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None,
                 local: bool = True,
                 html: bool = None):
    if local:
        message = localize(message, get_lang(update))

    parse_mode = None
    if html:
        parse_mode = 'HTML'

    if update.message is not None:
        update.message.reply_text(text=message, reply_markup=reply_markup, parse_mode=parse_mode)

    if update.callback_query is not None:
        context.bot.send_message(text=message, chat_id=update.callback_query.message.chat.id, reply_markup=reply_markup,
                                 parse_mode=parse_mode)


def datetime_to_db(d: datetime.datetime) -> str:
    return d.strftime('%Y-%m-%d')


def parse_date(d: str, lang='en') -> date:
    return dateparser.parse(d, languages=[lang]).date()


def parse_date_db(d: str) -> date:
    return dateparser.parse(d, date_formats=['%Y-%m-%d']).date()
