from internals import *
from maasser_state_management import *

import dateparser

from Database.MaasserUserDatabase import MaasserUserDatabase
from maasser_currency import MaasserCurrency
from ReplyMarkupHelper import ReplyMarkupHelper


def fun_maasser_give(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    reply_markup = ReplyKeyboardMarkup(
        [
            [localize('Yesterday', get_lang(update))],
            [localize('Today', get_lang(update))],
        ], one_time_keyboard=True)

    send_message("MASR: date", update, context, reply_markup)

    return MAASSER_GIVE_DATE


def fun_maasser_give_date(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    message = get_message(update)
    date = get_message_text(update)
    message.delete()

    try:
        context.chat_data['ADD'] = dateparser.parse(date, locales=['fr']).date().strftime('%Y-%m-%d')
    except (TypeError, ValueError):
        send_message('MASR: retry', update, context)
        return

    send_message("MASR: amount", update, context)

    return MAASSER_GIVE_AMOUNT


def fun_maasser_give_amount(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    message = get_message(update)
    amount = get_message_text(update)
    message.delete()

    try:
        if 'EUR' in amount or '€' in amount:
            amount = amount.replace('EUR', '').replace('€', '')
            amount = float(amount) / MaasserCurrency.get_exchanges_rates()['ILS:EUR']
        elif 'USD' in amount or '$' in amount:
            amount = amount.replace('USD', '').replace('$', '')
            amount = float(amount) / MaasserCurrency.get_exchanges_rates()['ILS:USD']
        amount_f = float(amount)
    except ValueError:
        send_message('MASR: retry', update, context)
        return

    data = {
        'date': context.chat_data['ADD'],
        'amount': amount_f
    }

    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.add_data(telegram_id, data)

    send_message("MASR: added", update, context)

    return MAASSER_NOMINAL


def fun_maasser_receive(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    reply_markup = ReplyKeyboardMarkup(
        [
            [localize('Yesterday', get_lang(update))],
            [localize('Today', get_lang(update))],
        ], one_time_keyboard=True)

    send_message("MASR: date", update, context, reply_markup)

    return MAASSER_RECEIVE_DATE


def fun_maasser_receive_date(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    message = get_message(update)
    date = get_message_text(update)
    message.delete()

    try:
        context.chat_data['ADD'] = dateparser.parse(date, locales=['fr']).date().strftime('%Y-%m-%d')
    except (TypeError, ValueError):
        send_message('MASR: retry', update, context)
        return

    send_message("MASR: amount", update, context)

    return MAASSER_RECEIVE_AMOUNT


def fun_maasser_receive_amount(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    message = get_message(update)
    amount = get_message_text(update)
    message.delete()

    try:
        if 'EUR' in amount or '€' in amount:
            amount = amount.replace('EUR', '').replace('€', '')
            amount = float(amount) / MaasserCurrency.get_exchanges_rates()['ILS:EUR']
        elif 'USD' in amount or '$' in amount:
            amount = amount.replace('USD', '').replace('$', '')
            amount = float(amount) / MaasserCurrency.get_exchanges_rates()['ILS:USD']
        amount_f = float(amount)
    except ValueError:
        send_message('MASR: retry', update, context)
        return

    data = {
        'date': context.chat_data['ADD'],
        'amount': -amount_f
    }

    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.add_data(telegram_id, data)

    send_message("MASR: added", update, context)

    return MAASSER_NOMINAL


