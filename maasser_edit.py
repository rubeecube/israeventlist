import json

from ReplyMarkupHelper import ReplyMarkupHelper
from internals import *
from maasser_state_management import *
from Database.MaasserUserDatabase import MaasserUserDatabase
from maasser_currency import MaasserCurrency


def fun_maasser_edit(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    send_message("MASR: password?", update, context)

    return MAASSER_EDIT


def fun_maasser_edit_print(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    password = get_message_text(update)
    get_message(update).delete()

    maasser_user_db = MaasserUserDatabase()

    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    data = maasser_user_db.consolidate(telegram_id, password)
    if data is None:
        send_message("MASR: invalid, bad password?", update, context)
        return MAASSER_NOMINAL

    data_reply = []
    for d in data:
        h = MaasserUserDatabase.fingerprint(d)
        s = f"{parse_date_db(d['date'])} - {d['amount']} {MaasserCurrency.currency_to_str(d['currency_current'])}"
        data_reply += [[s, h]]

    reply_markup = ReplyMarkupHelper.generic_build_reply_markup(
        data_reply,
        multi_select=False
    )

    send_message("MASR: choose edit", update, context, reply_markup=reply_markup)

    return MAASSER_EDIT_HANDLE


def fun_maasser_edit_handle(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    query = get_message_text(update)

    maasser_user_db = MaasserUserDatabase()

    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    maasser_user_db.remove_data(telegram_id, query)
    edit_message("MASR: removed", update, context)

    return MAASSER_NOMINAL