from internals import *
from maasser_state_management import *
from Database.MaasserUserDatabase import MaasserUserDatabase


async def fun_maasser_password_init(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    password = get_message_text(update)
    await get_message(update).delete()

    await send_message("MASR: password set", update, context)

    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.init(telegram_id, password)

    if not maasser_user:
        await send_message("MASR: error", update, context)
        return

    return MAASSER_NOMINAL
