from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Tuple, Optional, Union
from Globals import Globals
from Database.EventDatabase import EventDatabase
from Database.InterestDatabase import InterestDatabase
from Database.POIDatabase import POIDatabase


class ReplyMarkupHelper:
    @staticmethod
    def event_build_reply_markup(
            chosen_data=None,
            add_begin_button: Optional[List[Tuple]] = None,
            add_end_button: Optional[List[Tuple]] = None,
            only_selected=False,
            interest_id=None,
            poi_id=None,
            multi_select=True
    ) -> InlineKeyboardMarkup:
        event_db = EventDatabase()
        events = event_db.get(interest_id=interest_id, poi_id=poi_id)
        if len(events) == 0:
            events = event_db.get()

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

    @staticmethod
    def interests_build_reply_markup(
            chosen_data=None,
            show_level2=False,
            add_begin_button: Optional[List[Tuple]] = None,
            add_end_button: Optional[List[Tuple]] = None,
            only_selected=False,
            multi_select=True
    ) -> InlineKeyboardMarkup:
        interest_db = InterestDatabase()
        interests, parents = interest_db.get()
        max_len = max([len(x['name']) for x in list(interests.values())]) + 3 + len(Globals.EMOJI_OK)

        button_list = []
        button_selected = []

        if isinstance(add_begin_button, list):
            button_list += [[InlineKeyboardButton(text, callback_data=key) for (text, key) in add_begin_button]]

        for interest_level1 in interests.values():
            if interest_level1['id_parent'] is not None:
                continue
            button1 = InlineKeyboardButton("%s" % interest_level1['name'].ljust(max_len),
                                           callback_data=interest_level1['id'])

            if chosen_data is not None and str(interest_level1['id']) in chosen_data:
                button_selected += [[button1]]
                button2 = InlineKeyboardButton(Globals.EMOJI_CHECKED, callback_data=interest_level1['id'])
            else:
                button2 = InlineKeyboardButton(Globals.EMOJI_WHITE_SQUARE, callback_data=interest_level1['id'])

            if multi_select:
                button_list += [[button1, button2]]
            else:
                button_list += [[button1]]

            if show_level2:
                for interest_level2 in parents[interest_level1['id']]:
                    button1 = InlineKeyboardButton("-- %s" % interest_level2['name'].ljust(max_len),
                                                   callback_data=interest_level2['id'])

                    if chosen_data is not None and str(interest_level2['id']) in chosen_data:
                        button_selected += [[button1]]
                        button2 = InlineKeyboardButton(Globals.EMOJI_CHECKED, callback_data=interest_level2['id'])
                    else:
                        button2 = InlineKeyboardButton(Globals.EMOJI_WHITE_SQUARE, callback_data=interest_level2['id'])

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

    @staticmethod
    def poi_build_reply_markup(
            chosen_data=None,
            add_begin_button: Optional[List[Tuple]] = None,
            add_end_button: Optional[List[Tuple]] = None,
            only_selected=False,
            interest_id=None,
            multi_select=True
    ) -> InlineKeyboardMarkup:
        poi_db = POIDatabase()
        pois = poi_db.get(interest_id=interest_id)
        if len(pois) == 0:
            pois = poi_db.get()

        button_list = []
        button_selected = []

        if isinstance(add_begin_button, list):
            button_list += [[InlineKeyboardButton(text, callback_data=key) for (text, key) in add_begin_button]]

        for poi in pois.values():
            button1 = InlineKeyboardButton("%s" % poi['name'], callback_data=poi['id'])

            if chosen_data is not None and str(poi['id']) in chosen_data:
                button_selected += [[button1]]
                button2 = InlineKeyboardButton(Globals.EMOJI_CHECKED, callback_data=poi['id'])
            else:
                button2 = InlineKeyboardButton(Globals.EMOJI_WHITE_SQUARE, callback_data=poi['id'])

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

    @staticmethod
    def generic_build_reply_markup(
            data=None,
            chosen_data=None,
            add_end_button: Optional[List[Tuple]] = None,
            only_selected=False,
            return_selected=False,
            multi_select=True
    ) -> Union[InlineKeyboardMarkup, List]:

        button_list = []
        button_selected = []
        selected = []

        for i, d in enumerate(data):
            i = str(i)
            button1 = InlineKeyboardButton("%s" % d, callback_data=i)

            if chosen_data is not None and i in chosen_data:
                selected += [d]
                button_selected += [[button1]]
                button2 = InlineKeyboardButton(Globals.EMOJI_CHECKED, callback_data=i)
            else:
                button2 = InlineKeyboardButton(Globals.EMOJI_WHITE_SQUARE, callback_data=i)

            if multi_select:
                button_list += [[button1, button2]]
            else:
                button_list += [[button1]]

        if return_selected:
            return selected

        if isinstance(add_end_button, list):
            button_list += [[InlineKeyboardButton(text, callback_data=key) for (text, key) in add_end_button]]

        if only_selected:
            reply_markup = InlineKeyboardMarkup(button_selected, one_time_keyboard=True)
        else:
            reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

        return reply_markup

