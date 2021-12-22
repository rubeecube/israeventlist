from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Globals import Globals
from Database.InterestDatabase import InterestDatabase
from Localization import localize
from typing import List, Tuple


class Interests:
    @staticmethod
    def build_reply_markup(
            chosen_data=None,
            show_level2=False,
            add_begin_button: List[Tuple] | None = None,
            add_end_button: List[Tuple] | None = None,
            only_selected=False,
            multi_select=True
    ) -> InlineKeyboardMarkup:
        interest_db = InterestDatabase()
        interests, parents = interest_db.get_all()
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
