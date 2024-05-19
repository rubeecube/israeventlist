import json

from ReplyMarkupHelper import ReplyMarkupHelper
from internals import *
from maasser_state_management import *
from Database.MaasserUserDatabase import MaasserUserDatabase
from maasser_currency import MaasserCurrency
import prettytable as pt


def fun_maasser_list(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    send_message("MASR: password?", update, context)

    return MAASSER_LIST


def fun_maasser_list_print(update: Update, context: CallbackContext) -> int:
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

    max = 4000

    table_pt = pt.PrettyTable([
        localize('Fingerprint', get_lang(update)),
        localize('Date', get_lang(update)),
        localize('Comment', get_lang(update)),
        localize('MASR: amount table--format', get_lang(update)).format(
            MaasserCurrency.currency_to_str(maasser_user.currency)
        )
    ])
    table_pt.align['Amount'] = 'r'

    for d in data:
        try:
            comment = d['comment']
        except KeyError:
            comment = ""
        if d['data_type'] == 'GIVE':
            c = '-'
        else:
            c = '+'
        table_pt.add_row([
            MaasserUserDatabase.fingerprint(d),
            parse_date_db(d['date']),
            comment,
            f"{c}{MaasserCurrency.strip_currency_from_str(str(d['amount_original']))} {MaasserCurrency.currency_to_str(d['currency_current'])}",
        ])
        if len(str(table_pt)) > max:
            send_message(f'<pre>{table_pt}</pre>', update, context, html=True)

            table_pt = pt.PrettyTable([
                localize('Fingerprint', get_lang(update)),
                localize('Date', get_lang(update)),
                localize('Comment', get_lang(update)),
                localize('MASR: amount table--format', get_lang(update)).format(
                    MaasserCurrency.currency_to_str(maasser_user.currency)
                )
            ])
            table_pt.align['Amount'] = 'r'

    send_message(f'<pre>{table_pt}</pre>', update, context, html=True)

    return MAASSER_NOMINAL
