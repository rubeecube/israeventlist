from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Globals import Globals
from Database.EventDatabase import EventDatabase
from Localization import localize
from typing import List, Tuple


class Events:
    @staticmethod
    def build_reply_markup(
            chosen_data=None,
            add_begin_button: List[Tuple] | None = None,
            add_end_button: List[Tuple] | None = None,
            only_selected=False,
            interest_id=None,
            poi_id=None,
            multi_select=True
    ) -> InlineKeyboardMarkup:
        event_db = EventDatabase()
        events = event_db.get_all(interest_id=interest_id, poi_id=poi_id)
        if len(events) == 0:
            events = event_db.get_all()

        button_list = []
        button_selected = []

        if isinstance(add_begin_button, list):
            button_list += [[InlineKeyboardButton(text, callback_data=key) for (text, key) in add_begin_button]]

        for event in events.values():
            button1 = InlineKeyboardButton("%s" % event['name'], callback_data=event['id'])

            if chosen_data is not None and str(event['id']) in chosen_data:
                button_selected += [[button1]]
                button2 = InlineKeyboardButton(Globals.EMOJI_CHECKED, callback_data=event['id'])
            else:
                button2 = InlineKeyboardButton(Globals.EMOJI_WHITE_SQUARE, callback_data=event['id'])

            if multi_select:
                button_list += [[button1, button2]]
            else:
                button_list += [[button1]]

        if isinstance(add_end_button, list):
            button_list += [[InlineKeyboardButton(text, callback_data=key) for (text, key) in add_end_button]]

        if only_selected:
            reply_markup = InlineKeyboardMarkup(button_selected, one_time_keyboard=True)
        else:
            reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

        return reply_markup

