from telegram import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
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

from internals import *
from internals_admin import *
from StateManagement_admin import *

from Unit import POI, Interest

from Interests import Interests

from Database.POIDatabase import POIDatabase
from Database.InterestDatabase import InterestDatabase
from Localization import localize
from admin_add_event import *


def funa_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(localize("welcome admin", get_lang(update)))

    return AUTHENTICATED


def funa_commands(update: Update, context: CallbackContext) -> None | int:
    reply = get_commands_admin(get_lang(update), exclude=["/stop"])

    update.message.reply_text(localize("command_admin list", get_lang(update)), reply_markup=reply)

    return None


def funa_add(update: Update, context: CallbackContext) -> int:
    list_add = ['poi', 'interest', 'event']
    list_add = [(l, localize(l, get_lang(update))) for l in list_add]

    button_list = [[InlineKeyboardButton(text,  callback_data=key)] for (key, text) in list_add]
    reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

    update.message.reply_text(localize('admin add category', get_lang(update)), reply_markup=reply_markup)

    return ADD


def funa_handle_add(update: Update, context: CallbackContext) -> int:
    key = get_callback_message(update)

    if key == 'poi':
        return funa_handle_add_poi(update, context)

    if key == 'interest':
        return funa_handle_add_interest(update, context)

    if key == 'event':
        return funa_handle_add_event(update, context)


def funa_handle_add_interest(update: Update, context: CallbackContext) -> int:
    reply_markup = Interests.build_reply_markup(show_level2=False,
                                                add_begin_button=[(localize("no parent interest", get_lang(update)),
                                                                   "**NOPARENT**")])

    context.bot.send_message(text=localize('interest for add', get_lang(update)),
                             chat_id=update.callback_query.message.chat_id,
                             reply_markup=reply_markup)

    return INTEREST_ADD_PARENT


def funa_handle_interest_add_parent(update: Update, context: CallbackContext) -> int:
    id_parent = update.callback_query.data

    interest_db = InterestDatabase()
    interests, parents = interest_db.get_all()

    if id_parent == "**NOPARENT**":
        id_parent = None
    elif int(id_parent) not in interests.keys():
        context.bot.send_message(text=localize('error', get_lang(update)),
                                 chat_id=update.callback_query.message.chat_id)
        return AUTHENTICATED

    context.chat_data['INTEREST_ADD_id_parent'] = id_parent

    context.bot.edit_message_text(text=localize('saved', get_lang(update)),
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  inline_message_id=update.callback_query.inline_message_id)

    context.bot.send_message(text= localize('name of interest', get_lang(update)),
                             chat_id=update.callback_query.message.chat_id)

    return INTEREST_ADD_NAME


def funa_interest_add_name(update: Update, context: CallbackContext) -> int:
    message = update.message.text

    context.chat_data['INTEREST_ADD_name'] = message

    interest = Interest()
    interest.name = context.chat_data['INTEREST_ADD_name']
    interest.id_parent = context.chat_data['INTEREST_ADD_id_parent']

    context.chat_data.pop("INTEREST_ADD_name")
    context.chat_data.pop("INTEREST_ADD_id_parent")

    interest_database = InterestDatabase()
    interest_database.save(interest)

    update.message.reply_text(localize('saved', get_lang(update)))

    return AUTHENTICATED


def funa_handle_add_poi(update: Update, context: CallbackContext) -> int:
    reply_markup = Interests.build_reply_markup(show_level2=True)

    context.bot.send_message(text=localize('interest for add', get_lang(update)),
                             chat_id=update.callback_query.message.chat_id,
                             reply_markup=reply_markup)

    return POI_ADD_INTEREST


def funa_handle_poi_add_interest(update: Update, context: CallbackContext) -> int:
    interest_id = update.callback_query.data

    interest_db = InterestDatabase()
    interests, parents = interest_db.get_all()

    if int(interest_id) not in interests.keys():
        context.bot.send_message(text=localize('error', get_lang(update)),
                                 chat_id=update.callback_query.message.chat_id)
        return AUTHENTICATED

    context.chat_data['POI_ADD_interest_id'] = interest_id

    context.bot.edit_message_text(text=localize('saved', get_lang(update)),
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  inline_message_id=update.callback_query.inline_message_id)

    context.bot.send_message(text= localize('name of poi', get_lang(update)),
                             chat_id=update.callback_query.message.chat_id)

    return POI_ADD_NAME


def funa_handle_poi_add_name(update: Update, context: CallbackContext) -> int:
    message = update.message.text

    context.chat_data['POI_ADD_name'] = message

    update.message.reply_text(localize('desc of poi', get_lang(update)))

    return POI_ADD_DESC


def funa_handle_poi_add_desc(update: Update, context: CallbackContext) -> int:
    message = update.message.text

    context.chat_data['POI_ADD_description'] = message

    update.message.reply_text(localize('location of poi', get_lang(update)))

    return POI_ADD_LOCATION


def funa_handle_poi_add_location(update: Update, context: CallbackContext) -> int:
    context.chat_data['POI_ADD_latitude'] = str(update.effective_message.location.latitude)
    context.chat_data['POI_ADD_longitude'] = str(update.effective_message.location.longitude)

    update.message.reply_text(localize('address of poi', get_lang(update)))

    return POI_ADD_ADDRESS


def funa_handle_poi_add_address(update: Update, context: CallbackContext) -> int:
    message = update.message.text

    context.chat_data['POI_ADD_address'] = message

    poi = POI()
    poi.name = context.chat_data['POI_ADD_name']
    poi.description = context.chat_data['POI_ADD_description']
    poi.address = context.chat_data['POI_ADD_address']
    poi.latitude = context.chat_data['POI_ADD_latitude']
    poi.longitude = context.chat_data['POI_ADD_longitude']
    poi.interest_id = context.chat_data['POI_ADD_interest_id']

    context.chat_data.pop("POI_ADD_name")
    context.chat_data.pop("POI_ADD_description")
    context.chat_data.pop("POI_ADD_address")
    context.chat_data.pop("POI_ADD_latitude")
    context.chat_data.pop("POI_ADD_longitude")
    context.chat_data.pop("POI_ADD_interest_id")

    poi_database = POIDatabase()
    poi_database.save(poi)

    update.message.reply_text(localize('saved', get_lang(update)))

    return AUTHENTICATED


def funa_nominal(update: Update, context: CallbackContext) -> int:
    if update.message.text == localize("exit menu", get_lang(update)):
        update.message.reply_text(localize('inform commands', get_lang(update)))

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
            POI_ADD_ADDRESS: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_handle_poi_add_address)],
            POI_ADD_INTEREST: [CallbackQueryHandler(funa_handle_poi_add_interest)],
            POI_ADD_LOCATION: [MessageHandler(Filters.location & ~Filters.command & filter_admin, funa_handle_poi_add_location)],
            INTEREST_ADD_PARENT: [CallbackQueryHandler(funa_handle_interest_add_parent)],
            INTEREST_ADD_NAME: [MessageHandler(Filters.text & ~Filters.command & filter_admin, funa_interest_add_name)],

            EVENT_ADD_HANDLE_CHOICE: [CallbackQueryHandler(funa_handle_add_event_choice)],
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
