from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
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

from Unit import POI

from Interests import Interests

from Database import POIDatabase
from Localization import localize


def fun_start(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(localize("welcome admin", "fr"))

    return AUTHENTICATED


def fun_add(update: Update, context: CallbackContext) -> int:
    list_add = ['POI']

    button_list = [[InlineKeyboardButton("%s" % button,  callback_data=button)] for button in list_add]
    reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

    update.message.reply_text(localize('category', "fr"), reply_markup=reply_markup)

    return POI_ADD


def fun_add_poi(update: Update, context: CallbackContext) -> int:
    reply_markup = Interests.build_reply_markup(show_level2=True, add_end_button=False)

    update.message.reply_text(localize('interest for add', "fr"), reply_markup=reply_markup)

    return POI_ADD_INTEREST


def fun_handle_poi_add_interest(update: Update, context: CallbackContext) -> int:
    interest_id = update.callback_query.data

    context.chat_data['POI_ADD_interest_id'] = interest_id

    context.bot.edit_message_text(text=localize('thanks interests admin', "fr"),
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  inline_message_id=update.callback_query.inline_message_id)

    context.bot.send_message(text= localize('name of poi?', "fr"),
                             chat_id=update.callback_query.message.chat_id)

    return POI_ADD_NAME


def fun_handle_poi_add_name(update: Update, context: CallbackContext) -> int:
    message = update.message.text

    context.chat_data['POI_ADD_name'] = message

    update.message.reply_text(localize('description of poi?', "fr"))

    return POI_ADD_DESC


def fun_handle_poi_add_desc(update: Update, context: CallbackContext) -> int:
    message = update.message.text

    context.chat_data['POI_ADD_description'] = message

    update.message.reply_text(localize('location of poi?', "fr"))

    return POI_ADD_LOCATION


def fun_handle_poi_add_location(update: Update, context: CallbackContext) -> int:
    context.chat_data['POI_ADD_location'] = str(update.effective_message.location)

    update.message.reply_text(localize('address of poi?', "fr"))

    return POI_ADD_ADDRESS


def fun_handle_poi_add_address(update: Update, context: CallbackContext) -> int:
    message = update.message.text

    context.chat_data['POI_ADD_address'] = message

    poi = POI()
    poi.name = context.chat_data['POI_ADD_name']
    poi.description = context.chat_data['POI_ADD_description']
    poi.address = context.chat_data['POI_ADD_address']
    poi.location = context.chat_data['POI_ADD_location']
    poi.interest_id = context.chat_data['POI_ADD_interest_id']

    context.chat_data.pop("POI_ADD_name")
    context.chat_data.pop("POI_ADD_description")
    context.chat_data.pop("POI_ADD_address")
    context.chat_data.pop("POI_ADD_location")
    context.chat_data.pop("POI_ADD_interest_id")

    poi_database = POIDatabase()
    poi_database.save_poi(poi)

    update.message.reply_text(localize('Saved', "fr"))

    return AUTHENTICATED


def main():
    persistence = PicklePersistence(filename='Storage/IsraEventListAdmin_bot')
    updater = Updater(TOKEN["IsraEventListAdmin_bot"], use_context=True, persistence=persistence)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', fun_start, Filters.user(username=["@RubeeCube", "@Olivertwistis"]))],
        states={
            POI_ADD: [MessageHandler(Filters.text & ~Filters.command, fun_add_poi)],
            POI_ADD_NAME: [MessageHandler(Filters.text & ~Filters.command, fun_handle_poi_add_name)],
            POI_ADD_DESC: [MessageHandler(Filters.text & ~Filters.command, fun_handle_poi_add_desc)],
            POI_ADD_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, fun_handle_poi_add_address)],
            POI_ADD_INTEREST: [CallbackQueryHandler(fun_handle_poi_add_interest)],
            POI_ADD_LOCATION: [MessageHandler(Filters.location & ~Filters.command, fun_handle_poi_add_location)],
        },
        name="IsraEventListAdmin_bot",
        fallbacks=[CommandHandler('add', fun_add)],
        persistent=True,
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
