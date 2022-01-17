from telegram import BotCommand
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
)

from typing import Optional

import Database
from Storage.config import TOKEN

from internals import *
from Database.MaasserUserDatabase import MaasserUserDatabase

from maasser_state_management import *
from maasser_give import *
from maasser_login import *
from maasser_view import *


def get_maasser_raw_commands(lang="fr"):
    commands = []
    for command in ["commands", "don", "salaire", "maasser", "contact", "details", "stop"]:
        commands += [
            ("/%s" % command, "%s" % localize("MASR: command %s" % command, lang)),
        ]
    return commands


def get_maasser_commands(lang="fr", exclude=None):
    button_list = []
    for command, desc in get_raw_commands(lang):
        if exclude is not None and command in exclude:
            continue
        button_list += [[
            KeyboardButton("%s - %s" % (command, desc)),
        ]]
    button_list += [[
        KeyboardButton(localize("exit menu", lang))
    ]]

    reply = ReplyKeyboardMarkup(button_list, one_time_keyboard=True)

    return reply


def fun_maasser_start(update: Update, context: CallbackContext) -> Optional[int]:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    send_message("MASR: welcome text", update, context)
    send_message("MASR: user found", update, context)

    return MAASSER_NOMINAL


def fun_maasser_percentage(update: Update, context: CallbackContext) -> Optional[int]:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    send_message("MASR: percentage ask", update, context)

    return MAASSER_PERCENTAGE


def fun_maasser_percentage_change(update: Update, context: CallbackContext) -> Optional[int]:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        send_message("MASR: welcome text", update, context)
        send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    amount_original = get_message_text(update)

    try:
        amount_i = int(amount_original)
    except ValueError:
        send_message("MASR: error", update, context)
        return MAASSER_NOMINAL

    if amount_i < 0 or amount_i > 100:
        send_message("MASR: error", update, context)
        return MAASSER_NOMINAL

    if maasser_user_db.set_maasser(telegram_id, amount_i):
        send_message("MASR: changed", update, context)
    else:
        send_message("MASR: error", update, context)

    return MAASSER_NOMINAL


def fun_maasser_commands(update: Update, context: CallbackContext) -> Optional[int]:
    reply = get_maasser_commands(get_lang(update), exclude=["/stop"])

    send_message("MASR: command list", update, context, reply_markup=reply)

    return MAASSER_NOMINAL


def fun_maasser_finish_init(update: Update, context: CallbackContext) -> int:

    return MAASSER_NOMINAL


def fun_maasser_nominal(update: Update, context: CallbackContext) -> int:
    if update.message.text == localize("exit menu", get_lang(update)):
        send_message('inform commands', update, context)

    return MAASSER_NOMINAL


def fun_maasser_stop(update: Update, context: CallbackContext) -> int:
    unsubscribe_all(update, context)

    send_message("goodbye text", update, context)

    return ConversationHandler.END


def fun_maasser_contact(update: Update, context: CallbackContext) -> None:
    send_message("contact us", update, context)

    update.message.reply_text("https://telegram.me/RubeeCube")

    return


def fun_maasser_details(update: Update, context: CallbackContext) -> None:
    send_message("MASR: details", update, context)

    return


def fun_maasser_details2(update: Update, context: CallbackContext) -> None:
    send_message("MASR: details2", update, context)

    return


def main():
    persistence = PicklePersistence(filename='Storage/Maasser_bot')
    updater = Updater(TOKEN["Maasser_bot"], use_context=True, persistence=persistence)
    Database.Database.path = 'Storage/Maasser_bot.db'

    for lang in ["fr", "il", "en"]:
        updater.bot.set_my_commands([BotCommand(c, d) for (c, d) in get_maasser_raw_commands(lang)])

    updater.bot.set_my_commands([BotCommand(c, d) for (c, d) in get_maasser_raw_commands(lang)])

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', fun_maasser_start),
            CommandHandler('contact', fun_maasser_contact),
        ],
        states={
            MAASSER_NOMINAL: [MessageHandler(Filters.all & ~Filters.command, fun_maasser_nominal)],
            MAASSER_PASSWORD_INIT: [MessageHandler(Filters.all & ~Filters.command, fun_maasser_password_init)],
            MAASSER_GIVE_AMOUNT: [MessageHandler(Filters.all & ~Filters.command, fun_maasser_give_amount)],
            MAASSER_GIVE_DATE: [MessageHandler(Filters.all & ~Filters.command, fun_maasser_give_date)],
            MAASSER_RECEIVE_AMOUNT: [MessageHandler(Filters.all & ~Filters.command, fun_maasser_receive_amount)],
            MAASSER_RECEIVE_DATE: [MessageHandler(Filters.all & ~Filters.command, fun_maasser_receive_date)],
            MAASSER_VIEW: [MessageHandler(Filters.all & ~Filters.command, fun_maasser_view_print)],
            MAASSER_PERCENTAGE: [MessageHandler(Filters.all & ~Filters.command, fun_maasser_percentage_change)],
        },
        name="Maasser_bot",
        fallbacks=[
            CommandHandler('stop', fun_maasser_stop),
            CommandHandler('commands', fun_maasser_commands),
            CommandHandler('contact', fun_maasser_contact),
            CommandHandler('details', fun_maasser_details),
            CommandHandler('details2', fun_maasser_details2),
            CommandHandler('give', fun_maasser_give),
            CommandHandler('don', fun_maasser_give),
            CommandHandler('receive', fun_maasser_receive),
            CommandHandler('salaire', fun_maasser_receive),
            CommandHandler('view', fun_maasser_view),
            CommandHandler('resume', fun_maasser_view),
            CommandHandler('maasser', fun_maasser_percentage),
        ],
        persistent=True,
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    return updater


if __name__ == '__main__':
    updater = main()
    updater.idle()
