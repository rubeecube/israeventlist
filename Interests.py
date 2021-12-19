from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Globals import Globals
from Database.InterestDatabase import InterestDatabase
from Localization import localize


class Interests:
    @staticmethod
    def build_reply_markup_edit(chosen_data, show_level2=False, add_end_button=True, only_selected=False):
        event_db = InterestDatabase()
        interests, parents = event_db.get_interests()
        max_len = max([len(x['name']) for x in list(interests.values())]) + 3 + len(Globals.EMOJI_OK)

        button_list = []
        button_selected = []
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

            button_list += [[button1, button2]]

            if show_level2:
                for interest_level2 in parents[interest_level1['id']]:
                    button1 = InlineKeyboardButton("%s" % interest_level2['name'].ljust(max_len),
                                                   callback_data=interest_level2['id'])

                    if chosen_data is not None and str(interest_level2['id']) in chosen_data:
                        button_selected += [[button1]]
                        button2 = InlineKeyboardButton(Globals.EMOJI_CHECKED, callback_data=interest_level2['id'])
                    else:
                        button2 = InlineKeyboardButton(Globals.EMOJI_WHITE_SQUARE, callback_data=interest_level2['id'])

                    button_list += [[button1, button2]]

        if add_end_button:
            button_list += [[InlineKeyboardButton(localize('finish interests', 'fr'), callback_data="***END***")]]

        if only_selected:
            reply_markup = InlineKeyboardMarkup(button_selected, one_time_keyboard=True)
        else:
            reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

        return reply_markup
