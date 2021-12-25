from Localization import localize
from telegram import Update
from telegram.ext import CallbackContext
from internals import *
from internals_admin import *
from Globals import Globals
from StateManagement_admin import *
import dateparser
from dateutil import parser
from Interests import Interests
from POIs import POIs
from Database.InterestDatabase import InterestDatabase
from Database.POIDatabase import POIDatabase
from Database.EventDatabase import EventDatabase
from Unit import Event
import json


def event_categories(update):
    return [
        localize('description', get_lang(update)),
        localize('time', get_lang(update)),
        localize('recurrence', get_lang(update)),
    ]


def event_days(update):
    return [
        localize('Monday', get_lang(update)),
        localize('Tuesday', get_lang(update)),
        localize('Wednesday', get_lang(update)),
        localize('Thursday', get_lang(update)),
        localize('Friday', get_lang(update)),
        localize('Saturday', get_lang(update)),
        localize('Sunday', get_lang(update)),
    ]


def funa_handle_add_event(update: Update, context: CallbackContext) -> int:
    data = event_categories(update)

    reply_markup = Globals.build_reply_markup_multiselect(
        data,
        add_end_button=[(localize('finish', get_lang(update)), "***END***")]
    )

    send_message_callback('info to add', update, context, reply_markup=reply_markup)

    return EVENT_ADD_HANDLE_CHOICE


def funa_handle_add_event_choice(update: Update, context: CallbackContext) -> int | None:
    chosen_data = []
    message = update.callback_query.message
    choice = get_callback_message(update)

    for inlinekb in message['reply_markup']['inline_keyboard']:
        if len(inlinekb) > 1 and inlinekb[1]['text'] == Globals.EMOJI_CHECKED:
            chosen_data += [inlinekb[1]['callback_data']]

    data = event_categories(update)

    if choice == "***END***":
        selected = Globals.build_reply_markup_multiselect(
            data,
            chosen_data=chosen_data,
            return_selected=True
        )
        context.chat_data['EVENT'] = {'optional': selected}

        send_message_callback('name of event', update, context)

        return EVENT_ADD_NAME

    if choice in chosen_data:
        chosen_data.remove(choice)
    else:
        chosen_data += [choice]

    reply_markup = Globals.build_reply_markup_multiselect(
        data,
        chosen_data=chosen_data,
        add_end_button=[(localize('finish', get_lang(update)), "***END***")]
    )

    edit_message('info to add', update, context, reply_markup=reply_markup)

    return


def funa_event_add_name(update: Update, context: CallbackContext) -> int:
    message = get_message(update)

    context.chat_data['EVENT']['name'] = message

    if localize('description', get_lang(update)) in context.chat_data['EVENT']['optional']:
        send_message('desc of event', update)

        return EVENT_ADD_DESC
    else:
        context.chat_data['EVENT']['description'] = None

        send_message('date', update)
        send_message('date format', update)

        return EVENT_ADD_DATE


def funa_event_add_desc(update: Update, context: CallbackContext) -> int:
    message = get_message(update)

    context.chat_data['EVENT']['desc'] = message

    send_message('date', update)
    send_message('date format', update)

    return EVENT_ADD_DATE


def funa_event_add_date(update: Update, context: CallbackContext) -> int | None:
    date = get_message(update)

    try:
        context.chat_data['EVENT']['date_event'] = dateparser.parse(date).date()
    except TypeError | ValueError:
        if 'date_error' in list(context.chat_data['EVENT'].keys()):
            context.chat_data['EVENT']['date_error'] += 1
            if context.chat_data['EVENT']['date_error'] >= 3:
                send_message('error', update)
                context.chat_data.pop('EVENT')
                return AUTHENTICATED
        else:
            context.chat_data['EVENT']['date_error'] = 1
        send_message('retry', update)
        send_message('date', update)
        send_message('date format', update)
        return

    if localize('time', get_lang(update)) in context.chat_data['EVENT']['optional']:
        send_message('hour', update)
        send_message('hour format', update)

        return EVENT_ADD_TIME
    else:
        context.chat_data['EVENT']['time_event'] = None

        if localize('recurrence', get_lang(update)) in context.chat_data['EVENT']['optional']:
            data = event_days(update)

            reply_markup = Globals.build_reply_markup_multiselect(
                data,
                add_end_button=[(localize('finish', get_lang(update)), "***END***")]
            )

            send_message('recurrence', update, reply_markup=reply_markup)

            return EVENT_ADD_HANDLE_RECURRENCE
        else:
            reply_markup = Interests.build_reply_markup(show_level2=True)

            send_message('interest for add',
                         update,
                         reply_markup=reply_markup)

            return EVENT_ADD_INTEREST


def funa_event_add_time(update: Update, context: CallbackContext) -> int | None:
    hour = get_message(update)

    try:
        context.chat_data['EVENT']['time_event'] = parser.parse(hour).time()
    except parser.ParserError:
        if 'time_error' in list(context.chat_data['EVENT'].keys()):
            context.chat_data['EVENT']['time_error'] += 1
            if context.chat_data['EVENT']['time_error'] >= 3:
                send_message('error', update)
                context.chat_data.pop('EVENT')
                return AUTHENTICATED
        else:
            context.chat_data['EVENT']['time_error'] = 1
        send_message('retry', update)
        send_message('hour', update)
        send_message('hour format', update)
        return

    if localize('recurrence', get_lang(update)) in context.chat_data['EVENT']['optional']:
        data = event_days(update)

        reply_markup = Globals.build_reply_markup_multiselect(
            data,
            add_end_button=[(localize('finish', get_lang(update)), "***END***")]
        )

        send_message('recurrence', update, reply_markup=reply_markup)

        return EVENT_ADD_HANDLE_RECURRENCE
    else:
        context.chat_data['EVENT']['recurrence'] = None

        reply_markup = Interests.build_reply_markup(show_level2=True)

        send_message('interest for add',
                     update,
                     reply_markup=reply_markup)

        return EVENT_ADD_INTEREST


def funa_handle_add_handle_recurrence(update: Update, context: CallbackContext) -> int | None:
    chosen_data = []
    message = update.callback_query.message
    choice = get_callback_message(update)

    for inlinekb in message['reply_markup']['inline_keyboard']:
        if len(inlinekb) > 1 and inlinekb[1]['text'] == Globals.EMOJI_CHECKED:
            chosen_data += [inlinekb[1]['callback_data']]

    data = event_days(update)

    if choice == "***END***":
        selected = Globals.build_reply_markup_multiselect(
            data,
            chosen_data=chosen_data,
            return_selected=True
        )
        context.chat_data['EVENT']['recurrence'] = selected

        reply_markup = Interests.build_reply_markup(show_level2=True)

        send_message_callback('interest for add',
                     update,
                     context,
                     reply_markup=reply_markup)

        return EVENT_ADD_INTEREST

    if choice in chosen_data:
        chosen_data.remove(choice)
    else:
        chosen_data += [choice]

    reply_markup = Globals.build_reply_markup_multiselect(
        data,
        chosen_data=chosen_data,
        add_end_button=[(localize('finish', get_lang(update)), "***END***")]
    )

    edit_message('recurrence', update, context, reply_markup=reply_markup)

    return EVENT_ADD_HANDLE_RECURRENCE


def funa_handle_event_add_interest(update: Update, context: CallbackContext) -> int:
    interest_id = get_callback_message(update)

    interest_db = InterestDatabase()
    interests, parents = interest_db.get_all()

    if int(interest_id) not in interests.keys():
        send_message_callback('error', update, context)
        return AUTHENTICATED

    context.chat_data['EVENT']['interest_id'] = interest_id

    reply_markup = Interests.build_reply_markup(show_level2=True, only_selected=True)

    edit_message('saved', update, context, reply_markup=reply_markup)

    reply_markup = POIs.build_reply_markup(interest_id=interest_id)

    send_message_callback('poi for add',
                          update,
                          context,
                          reply_markup=reply_markup)

    return EVENT_ADD_POI


def funa_handle_event_add_poi(update: Update, context: CallbackContext) -> int:
    poi_id = get_callback_message(update)

    poi_db = POIDatabase()
    pois = poi_db.get_all()

    if int(poi_id) not in pois.keys():
        send_message_callback('error', update, context)
        return AUTHENTICATED

    context.chat_data['EVENT']['poi_id'] = poi_id

    event = Event()
    event.name = context.chat_data['EVENT']['name']
    event.description = context.chat_data['EVENT']['description']
    event.interest_id = context.chat_data['EVENT']['interest_id']
    event.poi_id = context.chat_data['EVENT']['poi_id']
    event.date_event = str(context.chat_data['EVENT']['date_event'])
    event.time_event = str(context.chat_data['EVENT']['time_event'])
    event.recurrence = json.dumps(context.chat_data['EVENT']['recurrence'])

    context.chat_data.pop("EVENT")

    event_database = EventDatabase()
    event_database.save(event)

    edit_message('saved', update, context)

    return AUTHENTICATED