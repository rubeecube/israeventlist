from internals_admin import *
from StateManagement_admin import *
from ReplyMarkupHelper import ReplyMarkupHelper
from Database.InterestDatabase import InterestDatabase
from Database.POIDatabase import POIDatabase
from Unit import POI


def funa_handle_add_poi(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyMarkupHelper.interests_build_reply_markup(show_level2=True)

    send_message('interest for add', update, context, reply_markup=reply_markup)

    return POI_ADD_INTEREST


def funa_handle_poi_add_interest(update: Update, context: CallbackContext) -> int:
    interest_id = get_message_text(update)

    interest_db = InterestDatabase()
    interests, parents = interest_db.get()

    if int(interest_id) not in interests.keys():
        context.bot.send_message(text=localize('error', get_lang(update)),
                                 chat_id=update.callback_query.message.chat_id)
        return AUTHENTICATED

    context.chat_data['POI_ADD_interest_id'] = interest_id

    edit_message('saved', update, context)

    send_message('name of poi', update, context)

    return POI_ADD_NAME


def funa_handle_poi_add_name(update: Update, context: CallbackContext) -> int:
    message = get_message_text(update)

    context.chat_data['POI_ADD_name'] = message

    send_message('desc of poi', update, context)

    return POI_ADD_DESC


def funa_handle_poi_add_desc(update: Update, context: CallbackContext) -> int:
    message = get_message_text(update)

    context.chat_data['POI_ADD_description'] = message

    send_message('location of poi', update, context)

    return POI_ADD_LOCATION


def funa_handle_poi_add_location(update: Update, context: CallbackContext) -> int:
    context.chat_data['POI_ADD_latitude'] = str(update.effective_message.location.latitude)
    context.chat_data['POI_ADD_longitude'] = str(update.effective_message.location.longitude)

    send_message('address of poi', update, context)

    return POI_ADD_ADDRESS


def funa_handle_poi_add_address(update: Update, context: CallbackContext) -> int:
    message = get_message_text(update)

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

    send_message('saved', update, context)

    return AUTHENTICATED
