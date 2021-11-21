import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
    CallbackContext,
)

from tokens import TOKEN

from internals import *
from StateManagement import *

from Data.Interests import Interests


def fun_start(update: Update, context: CallbackContext) -> int:
    initialize(update, context)

    update.message.reply_text(localize("welcome text", "fr"))

    return STARTED


def fun_ask_phone(update: Update, context: CallbackContext) -> None:
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(localize('Share contact', "fr"), request_contact=True)]])

    update.message.reply_text(localize('retrieve phone', "fr"), reply_markup=reply_markup)

    return HANDLE_PHONE


def fun_handle_phone(update: Update, context: CallbackContext) -> None:
    if update.effective_message.contact is None:
        return fun_handle_phone_err(update, context)

    print(update.effective_message.contact.phone_number)

    update.message.reply_text(localize('retrieve phone', "fr"))

    return AFTER_PHONE


def fun_handle_phone_err(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(localize('phone not retrieved, we try later', "fr"))

    return AFTER_PHONE


def fun_ask_location(update: Update, context: CallbackContext) -> None:
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(localize('Share location', "fr"), request_location=True)]])

    update.message.reply_text(localize('retrieve location', "fr"), reply_markup=reply_markup)

    return HANDLE_LOCATION


def fun_handle_location(update: Update, context: CallbackContext) -> None:
    if update.effective_message.location is None:
        return fun_handle_location_err(update, context)

    print(update.effective_message.location)

    update.message.reply_text(localize('retrieve location', "fr"))

    return AFTER_LOCATION


def fun_handle_location_err(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(localize('location not retrieved, we try later', "fr"))

    return AFTER_LOCATION


def fun_ask_interests(update: Update, context: CallbackContext) -> None:
    button_list = [InlineKeyboardButton(choice, callbackquery=choice) for choice in Interests.BASE_INTERESTS.keys()]
    button_list += [InlineKeyboardButton("Terminer", callbackquery="***END***")]
    reply_markup = InlineKeyboardMarkup([button_list])

    update.message.reply_text(localize('retrieve interests', "fr"), reply_markup=reply_markup)

    return HANDLE_INTERESTS


def fun_handle_interests(update: Update, context: CallbackContext) -> None:
    print(update.callback_query)
    print(update.callback_query.data)
    print(update.callback_query.message)

    return HANDLE_INTERESTS


def fun_cancel(update: Update, context: CallbackContext) -> int:
    unsubscribe_all(update, context)

    update.message.reply_text(localize("goodbye text", "fr"))

    return ConversationHandler.END


def main():
    persistence = PicklePersistence(filename='IsraEventList_bot')
    updater = Updater(TOKEN["IsraEventList_bot"], use_context=True, persistence=persistence)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', fun_start)],
        states={
            ASK_PHONE: [MessageHandler(Filters.text & ~Filters.command, fun_ask_phone)],
            HANDLE_PHONE: [MessageHandler(~Filters.command , fun_handle_phone)],
            ASK_LOCATION: [MessageHandler(~Filters.command, fun_ask_phone)],
            HANDLE_LOCATION: [MessageHandler(~Filters.command, fun_handle_location)],
            ASK_INTERESTS: [MessageHandler(~Filters.command, fun_ask_interests)],
            HANDLE_INTERESTS: [CallbackQueryHandler(fun_handle_interests)],
            #NOMINAL: [MessageHandler(Filters.all, fun_nominal)],
            #HELP: [MessageHandler(~Filters.command, fun_help)],
        },
        name="IsraEventList_bot",
        fallbacks=[CommandHandler('cancel', fun_cancel)],
        persistent=True,
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
