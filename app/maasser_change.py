from typing import Optional
from internals import *
from Database.MaasserUserDatabase import MaasserUserDatabase
from maasser_currency import MaasserCurrency

from maasser_state_management import *


async def fun_maasser_percentage(update: Update, context: CallbackContext) -> Optional[int]:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        await send_message("MASR: welcome text", update, context)
        await send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    await send_message("MASR: percentage ask", update, context)

    return MAASSER_PERCENTAGE


async def fun_maasser_percentage_change(update: Update, context: CallbackContext) -> Optional[int]:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        await send_message("MASR: welcome text", update, context)
        await send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    amount_original = get_message_text(update)

    try:
        amount_i = int(amount_original)
    except ValueError:
        await send_message("MASR: error", update, context)
        return MAASSER_NOMINAL

    if amount_i < 0 or amount_i > 100:
        await send_message("MASR: error", update, context)
        return MAASSER_NOMINAL

    if maasser_user_db.set_maasser(telegram_id, amount_i):
        await send_message("MASR: changed", update, context)
    else:
        await send_message("MASR: error", update, context)

    return MAASSER_NOMINAL


async def fun_maasser_currency(update: Update, context: CallbackContext) -> Optional[int]:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        await send_message("MASR: welcome text", update, context)
        await send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    await send_message("MASR: currency ask", update, context)

    return MAASSER_CURRENCY


async def fun_maasser_currency_password(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        await send_message("MASR: welcome text", update, context)
        await send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    currency = get_message_text(update)
    currency_i = MaasserCurrency.str_to_currency(currency)

    if currency_i is None:
        await send_message("MASR: error", update, context)
        return MAASSER_NOMINAL

    context.chat_data['CHANGE'] = {'currency': currency_i}

    await send_message("MASR: password?", update, context)

    return MAASSER_CURRENCY_PASSWORD


async def fun_maasser_currency_change(update: Update, context: CallbackContext) -> Optional[int]:
    telegram_id = update.effective_user.id
    password = get_message_text(update)
    await get_message(update).delete()

    maasser_user_db = MaasserUserDatabase()

    data = maasser_user_db.consolidate(telegram_id, password)
    if data is None:
        await send_message("MASR: invalid, bad password?", update, context)
        return MAASSER_NOMINAL

    currency = context.chat_data['CHANGE']['currency']
    try:
        if maasser_user_db.set_currency(telegram_id, currency, password):
            await send_message("MASR: changed", update, context)
        else:
            await send_message("MASR: error", update, context)
    except Exception:
            await send_message("MASR: error", update, context)

    return MAASSER_NOMINAL
