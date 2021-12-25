from telegram import BotCommand
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
)

from Storage.config import TOKEN

from user_search import *
from user_location import *
from user_interests import *
from user_phone import *


def fun_start(update: Update, context: CallbackContext) -> None | int:
    initialize(update, context)

    send_message("welcome text", update, context)

    return fun_commands(update, context)


def fun_commands(update: Update, context: CallbackContext) -> None | int:
    reply = get_commands(get_lang(update), exclude=["/stop"])

    send_message("command list", update, context, reply_markup=reply)

    return NOMINAL


def fun_finish_init(update: Update, context: CallbackContext) -> int:

    return NOMINAL


def fun_nominal(update: Update, context: CallbackContext) -> int:
    if update.message.text == localize("exit menu", get_lang(update)):
        send_message('inform commands', update, context)

    return NOMINAL


def fun_stop(update: Update, context: CallbackContext) -> int:
    unsubscribe_all(update, context)

    send_message("goodbye text", update, context)

    return ConversationHandler.END


def fun_contact(update: Update, context: CallbackContext) -> None:
    send_message("contact us", update, context)

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
            HANDLE_PHONE: [MessageHandler(~Filters.command, fun_handle_phone)],
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
