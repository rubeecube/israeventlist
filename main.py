import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, KeyboardButton, BotCommand
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

from Storage.config import TOKEN

from internals import *
from StateManagement import *

from Interests import Interests
from Globals import Globals
from Database import InterestDatabase
from Localization import localize
from user_search import *


def fun_start(update: Update, context: CallbackContext) -> None | int:
    initialize(update, context)

    update.message.reply_text(localize("welcome text", get_lang(update)))

    return fun_commands(update, context)


def fun_commands(update: Update, context: CallbackContext) -> None | int:
    reply = get_commands(get_lang(update), exclude=["/stop"])

    update.message.reply_text(localize("command list", get_lang(update)), reply_markup=reply)

    return NOMINAL


def fun_ask_phone(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(localize('share contact', get_lang(update)), request_contact=True,
                                                        one_time_keyboard=True)]])

    update.message.reply_text(localize('retrieve phone', get_lang(update)), reply_markup=reply_markup)

    return HANDLE_PHONE


def fun_handle_phone(update: Update, context: CallbackContext) -> int:
    if update.effective_message.contact is None:
        return fun_handle_phone_err(update, context)

    save_phone(update, context)

    update.message.reply_text(localize('thanks phone', get_lang(update)))

    return fun_commands(update, context)


def fun_handle_phone_err(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(localize('phone not retrieved, we try later', get_lang(update)))

    return fun_commands(update, context)


def fun_ask_location(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(localize('share location', get_lang(update)), request_location=True, one_time_keyboard = True)]])

    update.message.reply_text(localize('retrieve location', get_lang(update)), reply_markup=reply_markup)

    return HANDLE_LOCATION


def fun_handle_location(update: Update, context: CallbackContext) -> int:
    if update.effective_message.location is None:
        return fun_handle_location_err(update, context)

    save_location(update, context)

    update.message.reply_text(localize('thanks location', get_lang(update)))

    return fun_commands(update, context)


def fun_handle_location_err(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(localize('location not retrieved, we try later', get_lang(update)))

    return fun_commands(update, context)


def fun_ask_interests(update: Update, context: CallbackContext) -> int:
    interests = get_interests(update, context)

    reply_markup = Interests.build_reply_markup(interests,
                                                add_end_button=[(localize('finish', 'fr'), "***END***")])

    update.message.reply_text(localize('retrieve interests', get_lang(update)), reply_markup=reply_markup)

    return HANDLE_INTERESTS


def fun_handle_interests(update: Update, context: CallbackContext) -> int:
    chosen_data = []
    message = update.callback_query.message

    for inlinekb in message['reply_markup']['inline_keyboard']:
        if len(inlinekb) > 1 and inlinekb[1]['text'] == Globals.EMOJI_CHECKED:
            chosen_data += [inlinekb[1]['callback_data']]

    if update.callback_query.data == "***END***":
        save_interests(update, context, chosen_data)

        context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                              message_id=update.callback_query.message.message_id,
                                              inline_message_id=update.callback_query.inline_message_id,
                                              reply_markup=Interests.build_reply_markup(
                                                  chosen_data,
                                                  only_selected=True
                                              ))

        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=localize('thanks interests', 'fr'))

        context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                 text=localize("command list", get_lang(update)),
                                 reply_markup=get_commands(get_lang(update), exclude=["/stop"]))

        return NOMINAL

    if update.callback_query.data in chosen_data:
        chosen_data.remove(update.callback_query.data)
    else:
        chosen_data += [update.callback_query.data]

    context.bot.edit_message_reply_markup(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        inline_message_id=update.callback_query.inline_message_id,
        reply_markup=Interests.build_reply_markup(chosen_data,
                                                  add_end_button=[(localize('finish', get_lang(update)),
                                                                   "***END***")]))
    return HANDLE_INTERESTS


def fun_finish_init(update: Update, context: CallbackContext) -> int:

    return NOMINAL


def fun_nominal(update: Update, context: CallbackContext) -> int:
    if update.message.text == localize("exit menu", get_lang(update)):
        update.message.reply_text(localize('inform commands', get_lang(update)))

    return NOMINAL


def fun_stop(update: Update, context: CallbackContext) -> int:
    unsubscribe_all(update, context)

    update.message.reply_text(localize("goodbye text", get_lang(update)))

    return ConversationHandler.END


def fun_contact(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(localize("contact us", get_lang(update)))

    update.message.reply_text("https://telegram.me/RubeeCube")

    return fun_commands(update, context)


def main():
    persistence = PicklePersistence(filename='Storage/IsraEventList_bot')
    updater = Updater(TOKEN["IsraEventList_bot"], use_context=True, persistence=persistence)

    for lang in ["fr", "il", "en"]:
        updater.bot.set_my_commands([BotCommand(c, d) for (c, d) in get_raw_commands(lang)])

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', fun_start),
            CommandHandler('contact', fun_contact)
        ],
        states={
            ASK_PHONE: [MessageHandler(Filters.text & ~Filters.command, fun_ask_phone)],
            HANDLE_PHONE: [MessageHandler(~Filters.command , fun_handle_phone)],
            ASK_LOCATION: [MessageHandler(~Filters.command, fun_ask_phone)],
            HANDLE_LOCATION: [MessageHandler(~Filters.command, fun_handle_location)],
            ASK_INTERESTS: [MessageHandler(~Filters.command, fun_ask_interests)],
            HANDLE_INTERESTS: [CallbackQueryHandler(fun_handle_interests)],
            FINISH_INIT: [MessageHandler(Filters.all, fun_finish_init)],
            NOMINAL: [MessageHandler(~Filters.command, fun_nominal)],
            SEARCH_CATEGORY: [CallbackQueryHandler(fun_handle_search)],
            SEARCH_HANDLE_EVENT_BY_POI: [CallbackQueryHandler(fun_handle_search_event_by_poi)],
            SEARCH_HANDLE_EVENT_BY_INTERESTS: [CallbackQueryHandler(fun_handle_search_event_by_interest)],
        },
        name="IsraEventList_bot",
        fallbacks=[
            CommandHandler('stop', fun_stop),
            CommandHandler('phone', fun_ask_phone),
            CommandHandler('location', fun_ask_location),
            CommandHandler('commands', fun_commands),
            CommandHandler('contact', fun_contact),
            CommandHandler('interests', fun_ask_interests),
            CommandHandler('search', fun_search)
        ],
        persistent=True,
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
