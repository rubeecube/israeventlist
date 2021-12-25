from internals import *

from StateManagement import *


def fun_ask_phone(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton(localize('share contact', get_lang(update)), request_contact=True, one_time_keyboard=True)]]
    )

    send_message('retrieve phone', update, context, reply_markup=reply_markup)

    return HANDLE_PHONE


def fun_handle_phone(update: Update, context: CallbackContext) -> int:
    if update.effective_message.contact is None:
        return fun_handle_phone_err(update, context)

    save_phone(update, context)

    send_message('thanks phone', update, context)

    return NOMINAL


def fun_handle_phone_err(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(localize('phone not retrieved, we try later', get_lang(update)))

    return NOMINAL
