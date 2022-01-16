from internals_admin import *
from Globals import Globals
import dateparser
from dateutil import parser
from ReplyMarkupHelper import ReplyMarkupHelper
from Unit import MaasserUser
import json
from maasser_state_management import *
from Database.MaasserUserDatabase import MaasserUserDatabase


def fun_maasser_password_init(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    password = get_message_text(update)
    get_message(update).delete()

    send_message("MASR: password set", update, context)

    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.init(telegram_id, password)

    return MAASSER_NOMINAL
