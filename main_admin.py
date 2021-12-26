from telegram import InlineKeyboardButton, BotCommand
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence
)

from Storage.config import TOKEN, ADMINS

from admin_add_event import *
from admin_add_interest import *
from admin_add_poi import *


def funa_start(update: Update, context: CallbackContext) -> int:
    send_message("welcome admin", update, context)

    return AUTHENTICATED


def funa_commands(update: Update, context: CallbackContext) -> None | int:
    reply = get_commands_admin(get_lang(update), exclude=["/stop"])

    send_message("command_admin list", update, context, reply_markup=reply)

    return None


def funa_add(update: Update, context: CallbackContext) -> int:
    list_add = ['poi', 'interest', 'event']
    list_add = [(el, localize(el, get_lang(update))) for el in list_add]

    button_list = [[InlineKeyboardButton(text,  callback_data=key)] for (key, text) in list_add]
    reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

    send_message('admin add category', update, context, reply_markup=reply_markup)

    return ADD


def funa_handle_add(update: Update, context: CallbackContext) -> int:
    key = get_message_text(update)

    if key == 'poi':
        return funa_handle_add_poi(update, context)

    if key == 'interest':
        return funa_handle_add_interest(update, context)

    if key == 'event':
        return funa_handle_add_event(update, context)


def funa_push(update: Update, context: CallbackContext) -> int:
    send_message('push', update, context)

    return PUSH


def funa_nominal(update: Update, context: CallbackContext) -> int:
    if get_message_text(update) == localize("exit menu", get_lang(update)):
        send_message('inform commands', update, context)

    return AUTHENTICATED


def main():
    persistence = PicklePersistence(filename='Storage/IsraEventListAdmin_bot')
    updater = Updater(TOKEN["IsraEventListAdmin_bot"], use_context=True, persistence=persistence)

    for lang in ["fr", "il", "en"]:
        updater.bot.set_my_commands([BotCommand(c, d) for (c, d) in get_raw_commands_admin(lang)])

    dispatcher = updater.dispatcher

    filter_admin = Filters.user(username=ADMINS)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', funa_start, filter_admin)],
        states={
            AUTHENTICATED: [MessageHandler(~Filters.command & filter_admin, funa_nominal)],
            ADD: [CallbackQueryHandler(funa_handle_add)],
            POI_ADD_NAME: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_handle_poi_add_name)],
            POI_ADD_DESC: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_handle_poi_add_desc)],
            POI_ADD_ADDRESS:
                [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_handle_poi_add_address)],
            POI_ADD_INTEREST: [CallbackQueryHandler(funa_handle_poi_add_interest)],
            POI_ADD_LOCATION:
                [MessageHandler(Filters.location & ~Filters.command & filter_admin, funa_handle_poi_add_location)],
            INTEREST_ADD_PARENT: [CallbackQueryHandler(funa_handle_interest_add_parent)],
            INTEREST_ADD_NAME: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_interest_add_name)],

            EVENT_ADD_NAME: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_event_add_name)],
            EVENT_ADD_DESC: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_event_add_desc)],
            EVENT_ADD_DATE: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_event_add_date)],
            EVENT_ADD_TIME: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_event_add_time)],
            EVENT_ADD_HANDLE_RECURRENCE: [CallbackQueryHandler(funa_handle_add_handle_recurrence)],
            EVENT_ADD_INTEREST: [CallbackQueryHandler(funa_handle_event_add_interest)],
            EVENT_ADD_POI: [CallbackQueryHandler(funa_handle_event_add_poi)],
        },
        name="IsraEventListAdmin_bot",
        fallbacks=[
            CommandHandler('add', funa_add, filter_admin),
            CommandHandler('push', funa_push, filter_admin),
            CommandHandler('commands', funa_commands, filter_admin),
        ],
        persistent=True,
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
