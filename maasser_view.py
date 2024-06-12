from internals import *
from maasser_state_management import *
from Database.MaasserUserDatabase import MaasserUserDatabase
import prettytable as pt
from maasser_currency import MaasserCurrency


def fun_maasser_view(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    send_message("MASR: password?", update, context)

    return MAASSER_VIEW


def fun_maasser_view_print(update: Update, context: CallbackContext) -> int:
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

    table_pt = pt.PrettyTable([
        localize('month', get_lang(update)),
        localize('MASR: amount table--format', get_lang(update)).format(
            MaasserCurrency.currency_to_str(maasser_user.currency)
        )
    ])
    table_pt.align['Symbol'] = 'l'
    table_pt.align['Amount'] = 'r'

    totalsum = 0
    table = {}
    for d in data:
        date = parse_date_db(d['date'])
        my = date.strftime("%m/%y")
        if my not in table:
            table[my] = 0
        amount = d['amount']
        if d['type'] == 'RECEIVE':
            amount *= -maasser_user.percentage/100
        table[my] += float(amount)
        totalsum += amount

    for k in list(table.keys()):
        table_pt.add_row([k, f'{table[k]:.2f}'])

    table_pt.add_row([localize("MASR: total", get_lang(update)), f'{totalsum:.2f}'])

    send_message(localize("MASR: percentage", get_lang(update)) + f": {maasser_user.percentage}%",
                 update, context, local=False)
    send_message("MASR: explain table", update, context)
    send_message(f'<pre>{table_pt}</pre>', update, context, html=True)

    return MAASSER_NOMINAL
