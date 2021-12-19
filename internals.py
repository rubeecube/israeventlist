from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    CallbackContext,

)
from Unit import User
from Database.UserDatabase import UserDatabase
from Localization import localize


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
        'language_code': update.effective_message.from_user.language_code,
    }

    user_database = UserDatabase()
    user_database.save_user(user)

    return


def save_phone(update: Update, context: CallbackContext) -> None:
    user_database = UserDatabase()

    user = user_database.get_user(update.effective_user.id)
    if user is None:
        user = User()
        user.telegram_id = update.effective_user.id

    user.user_data = context.user_data

    user.phone = update.effective_message.contact.phone_number

    user_database.save_user(user)
    return


def save_location(update: Update, context: CallbackContext) -> None:
    user_database = UserDatabase()

    user = user_database.get_user(update.effective_user.id)
    if user is None:
        user = User()
        user.telegram_id = update.effective_user.id

    user.user_data = context.user_data

    user.location = str(update.effective_message.location)

    user_database.save_user(user)

    return


def save_interests(update: Update, context: CallbackContext, interests) -> None:
    user_database = UserDatabase()

    user = user_database.get_user(update.effective_user.id)
    if user is None:
        user = User()
        user.interests = interests

    user.user_data = context.user_data

    user.interests = interests

    user_database.save_user(user)

    return


def get_interests(update: Update, context: CallbackContext) -> None | list:
    user_database = UserDatabase()

    user = user_database.get_user(update.effective_user.id)
    if user is None:
        return None

    return user.interests


def get_commands():
    button_list = []
    for command in ["interests", "phone", "location", "commands", "contact", "cancel"]:
        button_list += [[
            KeyboardButton("/%s - %s" % (command, localize("command %s" % command, "fr"))),
        ]]

    reply = ReplyKeyboardMarkup(button_list, one_time_keyboard=True)

    return reply

def set_jobs(update: Update, context: CallbackContext) -> None:
    return


def unsubscribe_all(update: Update, context: CallbackContext) -> None:
    return




