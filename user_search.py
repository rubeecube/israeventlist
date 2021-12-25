from internals import *

from Unit import Event
from ReplyMarkupHelper import ReplyMarkupHelper

from Database.POIDatabase import POIDatabase
from Database.EventDatabase import EventDatabase
from Database.InterestDatabase import InterestDatabase
from StateManagement import *


def search_list():
    return ['poi', 'interest']


def fun_search(update: Update, context: CallbackContext) -> int:
    list_add = search_list()

    reply_markup = ReplyMarkupHelper.generic_build_reply_markup(data=list_add, multi_select=False)

    send_message('search category', update, context, reply_markup=reply_markup)

    return SEARCH_CATEGORY


def fun_handle_search(update: Update, context: CallbackContext) -> int:
    key = get_message_text(update)
    try:
        if int(key) > len(search_list()):
            send_message('error', update, context)
            return NOMINAL
    except ValueError:
        send_message('error', update, context)
        return NOMINAL

    key = search_list()[int(key)]

    if key == 'poi':
        return fun_handle_search_poi(update, context)

    if key == 'interest':
        return fun_handle_search_interest(update, context)


def fun_handle_search_poi(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyMarkupHelper.poi_build_reply_markup(multi_select=False)

    send_message('poi for search', update, context, reply_markup=reply_markup)

    return SEARCH_HANDLE_EVENT_BY_POI


def fun_handle_search_interest(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyMarkupHelper.interests_build_reply_markup(multi_select=False)

    send_message('interests for search', update, context, reply_markup=reply_markup)

    return SEARCH_HANDLE_EVENT_BY_INTERESTS


def fun_handle_search_event_by_poi(update: Update, context: CallbackContext) -> int:
    poi_id = get_message_text(update)

    poi_db = POIDatabase()
    pois = poi_db.get()

    if int(poi_id) not in pois.keys():
        send_message('error', update, context)
        return NOMINAL

    event_db = EventDatabase()
    events = event_db.get(poi_id=poi_id)
    if len(events) == 0:
        send_message('no event found for poi, showing all', update, context)
        events = event_db.get()
    else:
        send_message('showing events', update, context)

    poi_database = POIDatabase()
    for event in events.values():
        send_message(Event.dict_to_str(event, get_lang(update)), update, context, local=False)
        poi = poi_database.get(element_id=event['poi_id'])
        context.bot.send_location(
            longitude=poi['longitude'],
            latitude=poi['latitude'],
            chat_id=update.callback_query.message.chat_id
        )

    send_message('inform commands', update, context)

    return NOMINAL


def fun_handle_search_event_by_interest(update: Update, context: CallbackContext) -> int:
    interest_id = get_message_text(update)

    interest_db = InterestDatabase()
    interests, parents = interest_db.get()

    if int(interest_id) not in interests.keys():
        send_message('error', update, context)
        return NOMINAL

    event_db = EventDatabase()
    events = event_db.get(interest_id=interest_id)
    if int(interest_id) in list(parents.keys()):
        for sub_interest in parents[int(interest_id)]:
            events_sub = event_db.get(interest_id=sub_interest['id'])
            for event_sub in events_sub.values():
                events[event_sub['id']] = event_sub
    if len(events) == 0:
        send_message('no event found for interest, showing all', update, context)
        events = event_db.get()
    else:
        send_message('showing events', update, context)

    poi_database = POIDatabase()
    for event in events.values():
        send_message(Event.dict_to_str(event, get_lang(update)), update, context, local=False)
        poi = poi_database.get(element_id=event['poi_id'])
        context.bot.send_location(
            longitude=poi['longitude'],
            latitude=poi['latitude'],
            chat_id=update.callback_query.message.chat_id
        )

    send_message('inform commands', update, context)

    return NOMINAL

