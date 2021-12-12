from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Globals import Globals
from Database.InterestDatabase import InterestDatabase


class Interests:
    @staticmethod
    def build_reply_markup(show_level2=False, add_end_button=True):
        event_db = InterestDatabase()
        interests, parents = event_db.get_interests()
        max_len = max([len(x['name']) for x in list(interests.values())]) + 3 + len(Globals.EMOJI_OK)

        if show_level2:
            interests_level = [[InlineKeyboardButton("%s" % interest_level1['name'].ljust(max_len),  callback_data=interest_level1['id'])] +
                               [InlineKeyboardButton("- %s" % interest_level2['name'].ljust(max_len),  callback_data=interest_level2['id'])
                                for interest_level2 in parents[interest_level1['id']]]
                               for interest_level1 in interests.values() if interest_level1['id_parent'] is None]
        else:
            interests_level = [[InlineKeyboardButton("%s" % interest_level1['name'].ljust(max_len),  callback_data=interest_level1['id'])]
                               for interest_level1 in interests.values() if interest_level1['id_parent'] is None]

        interests_level = [item for sublist in interests_level for item in sublist]

        button_list = [[button] for button in interests_level]
        if add_end_button:
            button_list += [[InlineKeyboardButton("Terminer", callback_data="***END***")]]
        reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

        return reply_markup

    @staticmethod
    def build_reply_markup_edit(chosen_data, show_level2=False):
        event_db = InterestDatabase()
        interests, parents = event_db.get_interests()
        max_len = max([len(x['name']) for x in list(interests.values())]) + 3 + len(Globals.EMOJI_OK)

        button_list = []
        for interest_level1 in interests.values():
            if interest_level1['id_parent'] is not None:
                continue
            if str(interest_level1['id']) in chosen_data:
                button_list += [[InlineKeyboardButton("%s %s" % (interest_level1['name'].ljust(max_len),
                                                                   Globals.EMOJI_OK),
                                                      callback_data=interest_level1['id'])]]
            else:
                button_list += [[InlineKeyboardButton("%s" % interest_level1['name'].ljust(max_len),  callback_data=interest_level1['id'])]]
            if show_level2:
                for interest_level2 in parents[interest_level1['id']]:
                    if str(interest_level2['id']) in chosen_data:
                        button_list += [[InlineKeyboardButton("- %s %s" % (interest_level2['name'].ljust(max_len),
                                                                           Globals.EMOJI_OK),
                                                              callback_data=interest_level2['id'])]]
                    else:
                        button_list += [
                            [InlineKeyboardButton("- %s" % interest_level2['name'].ljust(max_len), callback_data=interest_level2['id'])]]
        button_list += [[InlineKeyboardButton("Terminer", callback_data="***END***")]]
        reply_markup = InlineKeyboardMarkup(button_list, one_time_keyboard=True)

        return reply_markup
