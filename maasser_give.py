from typing import Literal
from internals import *
from maasser_state_management import *

from Database.MaasserUserDatabase import MaasserUserDatabase
from maasser_currency import MaasserCurrency


def fun_maasser_give_annex(update: Update, context: CallbackContext, return_status: int) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    send_message("MASR: comment", update, context)

    return return_status


def fun_maasser_give_annex_comment(update: Update, context: CallbackContext, return_status: int) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    message = get_message(update)
    comment = get_message_text(update)
    message.delete()

    context.chat_data['ADD'] = {
        'comment': comment
    }

    reply_markup = ReplyKeyboardMarkup(
        [
            [localize('Yesterday', get_lang(update))],
            [localize('Today', get_lang(update))],
        ], one_time_keyboard=True)

    send_message("MASR: date", update, context, reply_markup)

    return return_status


def fun_maasser_give_annex_date(update: Update, context: CallbackContext, return_status: int) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    message = get_message(update)
    date = get_message_text(update)
    print(message)
    print(date)
    message.delete()

    try:
        context.chat_data['ADD']['parsed_date'] = parse_date(date, get_lang(update))
        context.chat_data['ADD']['original_date'] = date
    except (TypeError, ValueError):
        send_message('MASR: error', update, context)
        return MAASSER_NOMINAL

    send_message(localize("MASR: amount--format", get_lang(update))
                 .format(MaasserCurrency.currency_to_str(maasser_user.currency)),
                 update, context, local=False)

    return return_status


def fun_maasser_give_annex_amount(update: Update, context: CallbackContext,
                                  data_type: Literal["GIVE", "RECEIVE"]) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    message = get_message(update)
    amount_original = get_message_text(update)
    message.delete()
    user_currency = maasser_user.currency

    amount = amount_original
    try:
        currency = MaasserCurrency.get_currency_from_str(amount)
        if currency is None:
            currency = user_currency
        amount = MaasserCurrency.strip_currency_from_str(amount)
        amount = MaasserCurrency.exchange(amount, currency, user_currency)
    except ValueError:
        send_message('MASR: error', update, context)
        return MAASSER_NOMINAL

    data = {
        'created': datetime_to_db(datetime.datetime.now()),
        'date': datetime_to_db(context.chat_data['ADD']['parsed_date']),
        'date_original': context.chat_data['ADD']['original_date'],
        'amount_original': amount_original,
        'currency_current': currency,
        'type': data_type,
        'comment': context.chat_data['ADD']['comment'],
        'amount': amount
    }

    maasser_user = maasser_user_db.add_data(telegram_id, data)
    if maasser_user:
        send_message("MASR: added", update, context)
    else:
        send_message("MASR: error", update, context)

    return MAASSER_NOMINAL


def fun_maasser_give(update: Update, context: CallbackContext) -> int:
    return fun_maasser_give_annex(update, context, MAASSER_GIVE_COMMENT)


def fun_maasser_give_comment(update: Update, context: CallbackContext) -> int:
    return fun_maasser_give_annex_comment(update, context, MAASSER_GIVE_DATE)


def fun_maasser_give_date(update: Update, context: CallbackContext) -> int:
    return fun_maasser_give_annex_date(update, context, MAASSER_GIVE_AMOUNT)


def fun_maasser_give_amount(update: Update, context: CallbackContext) -> int:
    return fun_maasser_give_annex_amount(update, context, 'GIVE')


def fun_maasser_receive(update: Update, context: CallbackContext) -> int:
    return fun_maasser_give_annex(update, context, MAASSER_RECEIVE_COMMENT)


def fun_maasser_receive_comment(update: Update, context: CallbackContext) -> int:
    return fun_maasser_give_annex_comment(update, context, MAASSER_RECEIVE_DATE)


def fun_maasser_receive_date(update: Update, context: CallbackContext) -> int:
    return fun_maasser_give_annex_date(update, context, MAASSER_RECEIVE_AMOUNT)


def fun_maasser_receive_amount(update: Update, context: CallbackContext) -> int:
    return fun_maasser_give_annex_amount(update, context, 'RECEIVE')
