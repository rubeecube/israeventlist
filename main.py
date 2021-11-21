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

from config import TOKEN

from internals import *
from StateManagement import *

from Data.Interests import Interests

EMOJI_SMILEY = "✔️"

def fun_start(update: Update, context: CallbackContext) -> int:
    initialize(update, context)

    update.message.reply_text(localize("welcome text", "fr"))

    return fun_ask_phone(update, context)


def fun_ask_phone(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(localize('Share contact', "fr"), request_contact=True, one_time_keyboard = True)]])

    update.message.reply_text(localize('retrieve phone', "fr"), reply_markup=reply_markup)

    return HANDLE_PHONE


def fun_handle_phone(update: Update, context: CallbackContext) -> int:
    if update.effective_message.contact is None:
        return fun_handle_phone_err(update, context)

    update.message.reply_text(update.effective_message.contact.phone_number)

    update.message.reply_text(localize('thanks phone', "fr"))

    return fun_ask_location(update, context)


def fun_handle_phone_err(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(localize('phone not retrieved, we try later', "fr"))

    return AFTER_PHONE


def fun_ask_location(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(localize('Share location', "fr"), request_location=True, one_time_keyboard = True)]])

    update.message.reply_text(localize('retrieve location', "fr"), reply_markup=reply_markup)

    return HANDLE_LOCATION


def fun_handle_location(update: Update, context: CallbackContext) -> int:
    if update.effective_message.location is None:
        return fun_handle_location_err(update, context)

    update.message.reply_text(str(update.effective_message.location))

    update.message.reply_text(localize('thanks location', "fr"))

    return fun_ask_interests(update, context)


def fun_handle_location_err(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(localize('location not retrieved, we try later', "fr"))

    return AFTER_LOCATION


def fun_ask_interests(update: Update, context: CallbackContext) -> int:
    max_len = max(map(len, Interests.BASE_INTERESTS.keys())) + 1 + len(EMOJI_SMILEY)

    button_list = [[InlineKeyboardButton(choice.ljust(max_len), callback_data=choice)] for choice in Interests.BASE_INTERESTS.keys()]
    button_list += [[InlineKeyboardButton("Terminer", callback_data="***END***")]]
    reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)
    print(reply_markup)

    update.message.reply_text(localize('retrieve interests', "fr"), reply_markup=reply_markup)

    return HANDLE_INTERESTS


def fun_handle_interests(update: Update, context: CallbackContext) -> int:
    chosen_data = []
    message = update.callback_query.message
    for inlinekb in message['reply_markup']['inline_keyboard']:
        if EMOJI_SMILEY in inlinekb[0]['text']:
            chosen_data += [inlinekb[0]['callback_data']]

    if update.callback_query.data == "***END***":
        print(chosen_data)

        context.bot.edit_message_text(text=localize('thanks interests', "fr"),
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      inline_message_id=update.callback_query.inline_message_id)

        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=str(chosen_data))

        return fun_finish_init(update, context)

    if update.callback_query.data in chosen_data:
        chosen_data.remove(update.callback_query.data)
    else:
        chosen_data += [update.callback_query.data]

    max_len = max(map(len, Interests.BASE_INTERESTS.keys())) + 1 + len(EMOJI_SMILEY)

    button_list = []
    for choice in Interests.BASE_INTERESTS.keys():
        if choice in chosen_data:
            button_list += [[InlineKeyboardButton("%s %s".ljust(max_len) % (choice, EMOJI_SMILEY), callback_data=choice)]]
        else:
            button_list += [[InlineKeyboardButton(choice.ljust(max_len), callback_data=choice)]]
    button_list += [[InlineKeyboardButton("Terminer", callback_data="***END***")]]
    reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

    context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          inline_message_id=update.callback_query.inline_message_id,
                                          reply_markup=reply_markup)
    return HANDLE_INTERESTS


def fun_finish_init(update: Update, context: CallbackContext) -> int:

    return NOMINAL


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
            FINISH_INIT: [MessageHandler(Filters.all, fun_finish_init)],
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
