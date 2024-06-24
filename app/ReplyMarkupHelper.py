from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Tuple, Optional, Union
from Globals import Globals


class ReplyMarkupHelper:
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
            if isinstance(d, list):
                d_str = d[0]
                callback_data = d[1]
            else:
                d_str = d
                callback_data = str(i)

            button1 = [InlineKeyboardButton("%s" % d_str, callback_data=callback_data)]

            if chosen_data is not None and i in chosen_data:
                selected += [d_str]
                button_selected += [button1]
                button2 = [InlineKeyboardButton(Globals.EMOJI_CHECKED, callback_data=callback_data)]
            else:
                button2 = [InlineKeyboardButton(Globals.EMOJI_WHITE_SQUARE, callback_data=callback_data)]

            if multi_select:
                button_list += [button1 + button2]
            else:
                button_list += [button1]

        if return_selected:
            return selected

        if isinstance(add_end_button, list):
            button_list += [[InlineKeyboardButton(text, callback_data=key) for (text, key) in add_end_button]]

        if only_selected:
            reply_markup = InlineKeyboardMarkup(button_selected)
        else:
            reply_markup = InlineKeyboardMarkup(button_list)

        return reply_markup
