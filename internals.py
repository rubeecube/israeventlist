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


def initialize(update: Update, context: CallbackContext) -> None:
    retrieve_info(update, context)
    set_jobs(update, context)
    return


def retrieve_info(update: Update, context: CallbackContext) -> None:
    print(update.effective_chat.first_name)
    print(update.effective_message.from_user.language_code)
    return


def set_jobs(update: Update, context: CallbackContext) -> None:
    return


def unsubscribe_all(update: Update, context: CallbackContext) -> None:
    return
