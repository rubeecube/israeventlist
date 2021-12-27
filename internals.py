from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from Unit import User
from Database.UserDatabase import UserDatabase
from Localization import localize
from typing import List, Optional


def get_lang(update: Update):
    try:
        return update.effective_message.from_user.language_code
    except AttributeError:
        pass

    try:
        return update.callback_query.from_user.language_code
    except AttributeError:
        pass

    return None


def initialize(update: Update, context: CallbackContext) -> None:
    save_info(update, context)
    set_jobs(update, context)
    return


def save_info(update: Update, context: CallbackContext) -> None:
    user = User()

    user.telegram_id = update.effective_user.id
    user.user_data = context.user_data
    user.misc = {
        'first_name': update.effective_chat.first_name,
        'language_code': get_lang(update),
    }

    user_database = UserDatabase()
    user_database.save(user)

    return


def save_phone(update: Update, context: CallbackContext) -> None:
    user_database = UserDatabase()

    user = user_database.get(update.effective_user.id)
    if user is None:
        user = User()
        user.telegram_id = update.effective_user.id

    user.user_data = context.user_data

    user.phone = update.effective_message.contact.phone_number

    user_database.save(user)
    return


def save_location(update: Update, context: CallbackContext) -> None:
    user_database = UserDatabase()

    user = user_database.get(update.effective_user.id)
    if user is None:
        user = User()
        user.telegram_id = update.effective_user.id

    user.user_data = context.user_data

    user.location = str(update.effective_message.location)

    user_database.save(user)

    return


def save_interests(update: Update, context: CallbackContext, interests) -> None:
    user_database = UserDatabase()

    user = user_database.get(update.effective_user.id)
    if user is None:
        user = User()
        user.interests = interests

    user.user_data = context.user_data

    user.interests = interests

    user_database.save(user)

    return


def get_interests(update: Update, context: CallbackContext) -> Optional[List]:
    user_database = UserDatabase()

    user = user_database.get(update.effective_user.id)
    if user is None:
        return None

    return user.interests


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


def set_jobs(update: Update, context: CallbackContext) -> None:
    return


def unsubscribe_all(update: Update, context: CallbackContext) -> None:
    return


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
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      inline_message_id=update.callback_query.inline_message_id,
                                      reply_markup=reply_markup)


def send_message(message, update: Update,
                 context: CallbackContext,
                 reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup = None,
                 local: bool = True):
    if local:
        message = localize(message, get_lang(update))

    if update.message is not None:
        update.message.reply_text(text=message, reply_markup=reply_markup)

    if update.callback_query is not None:
        context.bot.send_message(text=message, chat_id=update.callback_query.message.chat_id, reply_markup=reply_markup)


