from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import uuid
from typing import List, Tuple


class Globals:
    EMOJI_OK = "✔️"
    EMOJI_WHITE_SQUARE = "◻️"
    EMOJI_CHECKED = "✅"
    EMOJI_MAGEN_DAVID = "✡️"
    EMOJI_THUMBS_UP = "👍"

    @staticmethod
    def build_reply_markup_multiselect(
            data=None,
            chosen_data=None,
            add_end_button: List[Tuple] | None = None,
            only_selected=False,
            return_selected=False,
            multi_select=True
    ) -> InlineKeyboardMarkup | List:

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
