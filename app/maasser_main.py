import urllib3
from telegram import BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    PicklePersistence,
)

import Database
from Storage.config import TOKEN

from maasser_give import *
from maasser_login import *
from maasser_view import *
from maasser_change import *
from maasser_edit import *
from maasser_list import *


def get_maasser_raw_commands(lang="fr"):
    commands = []
    for command in ["commands", "recap", "don", "salaire", "show", "maasser", "devise", "edit", "contact", "details",
                    "stop"]:
        commands += [
            ("/%s" % command, "%s" % localize("MASR: command %s" % command, lang)),
        ]
    return commands


def get_maasser_commands(lang="fr", exclude=None):
    button_list = []
    for command, desc in get_maasser_raw_commands(lang):
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


async def fun_maasser_start(update: Update, context: CallbackContext) -> Optional[int]:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        await send_message("MASR: welcome text", update, context)
        await send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    await send_message("MASR: welcome text", update, context)
    await send_message("MASR: user found", update, context)

    return MAASSER_NOMINAL


async def fun_maasser_commands(update: Update, context: CallbackContext) -> Optional[int]:
    reply = get_maasser_commands(get_lang(update), exclude=["/stop"])

    await send_message("MASR: command list", update, context, reply_markup=reply)

    return MAASSER_NOMINAL


async def fun_maasser_finish_init(update: Update, context: CallbackContext) -> int:
    return MAASSER_NOMINAL


async def fun_maasser_nominal(update: Update, context: CallbackContext) -> int:
    if update.message.text == localize("exit menu", get_lang(update)):
        await send_message('inform commands', update, context)

    return MAASSER_NOMINAL


async def fun_maasser_stop(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is not None:
        maasser_user_db.erase(telegram_id)

    await send_message("goodbye text", update, context)

    return ConversationHandler.END


async def fun_maasser_contact(update: Update, context: CallbackContext) -> None:
    await send_message("contact us", update, context)
    await update.message.reply_text("https://telegram.me/RubeeCube")
    return


async def fun_maasser_details(update: Update, context: CallbackContext) -> None:
    await send_message("MASR: details", update, context)
    return


async def fun_maasser_details2(update: Update, context: CallbackContext) -> None:
    await send_message("MASR: details2", update, context)
    return


def main():
    persistence = PicklePersistence(filepath='Storage/Maasser_bot')
    application = Application.builder().token(TOKEN["Maasser_bot"]).persistence(persistence).build()
    Database.Database.path = 'Storage/Maasser_bot.db'

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', fun_maasser_start),
            CommandHandler('contact', fun_maasser_contact),
        ],
        states={
            MAASSER_NOMINAL: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                             fun_maasser_nominal)],
            MAASSER_PASSWORD_INIT: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                   fun_maasser_password_init)],
            MAASSER_GIVE_AMOUNT: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                 fun_maasser_give_amount)],
            MAASSER_GIVE_DATE: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                               fun_maasser_give_date)],
            MAASSER_GIVE_COMMENT: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                  fun_maasser_give_comment)],
            MAASSER_RECEIVE_AMOUNT: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                    fun_maasser_receive_amount)],
            MAASSER_RECEIVE_DATE: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                  fun_maasser_receive_date)],
            MAASSER_RECEIVE_COMMENT: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                     fun_maasser_receive_comment)],
            MAASSER_VIEW: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                          fun_maasser_view_print)],
            MAASSER_PERCENTAGE: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                fun_maasser_percentage_change)],
            MAASSER_CURRENCY: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                              fun_maasser_currency_password)],
            MAASSER_CURRENCY_PASSWORD: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                       fun_maasser_currency_change)],
            MAASSER_EDIT_HANDLE: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                                 fun_maasser_edit_handle)],
            MAASSER_LIST: [MessageHandler(filters.ALL & ~filters.COMMAND,
                                          fun_maasser_list_print)],

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
            CommandHandler('recap', fun_maasser_view),
            CommandHandler('maasser', fun_maasser_percentage),
            CommandHandler('devise', fun_maasser_currency),
            CommandHandler('edit', fun_maasser_edit),
            CommandHandler('show', fun_maasser_list),
        ],
        persistent=True,
        allow_reentry=True
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
