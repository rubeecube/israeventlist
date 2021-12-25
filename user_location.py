from internals import *

from StateManagement import *


def fun_ask_location(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton(localize('share location', get_lang(update)), request_location=True, one_time_keyboard=True)]]
    )

    send_message('retrieve location', update, context, reply_markup=reply_markup)

    return HANDLE_LOCATION


def fun_handle_location(update: Update, context: CallbackContext) -> int:
    if update.effective_message.location is None:
        return fun_handle_location_err(update, context)

    save_location(update, context)

    send_message('thanks location', update, context)

    return NOMINAL


def fun_handle_location_err(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(localize('location not retrieved, we try later', get_lang(update)))

    return NOMINAL

