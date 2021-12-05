from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,

)
from Localization.dispatch import localize
from StateManagement import *
from Data.User import User
from CustomerDatabase import CustomerDatabase


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

    customer_database = CustomerDatabase()
    customer_database.save_user(user)

    return


def save_phone(update: Update, context: CallbackContext) -> None:
    customer_database = CustomerDatabase()

    user = customer_database.get_user(update.effective_user.id)
    if user is None:
        user = User()
        user.telegram_id = update.effective_user.id

    user.user_data = context.user_data

    user.phone = update.effective_message.contact.phone_number

    customer_database.save_user(user)
    return


def save_location(update: Update, context: CallbackContext) -> None:
    customer_database = CustomerDatabase()

    user = customer_database.get_user(update.effective_user.id)
    if user is None:
        user = User()
        user.telegram_id = update.effective_user.id

    user.user_data = context.user_data

    user.location = str(update.effective_message.location)

    customer_database.save_user(user)

    return


def save_interests(update: Update, context: CallbackContext, interests) -> None:
    customer_database = CustomerDatabase()

    user = customer_database.get_user(update.effective_user.id)
    if user is None:
        user = User()
        user.interests = interests

    user.user_data = context.user_data

    user.interests = interests

    customer_database.save_user(user)

    return


def set_jobs(update: Update, context: CallbackContext) -> None:
    return


def unsubscribe_all(update: Update, context: CallbackContext) -> None:
    return




