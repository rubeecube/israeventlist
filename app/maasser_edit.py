from internals import *
from maasser_state_management import *
from Database.MaasserUserDatabase import MaasserUserDatabase


async def fun_maasser_edit(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id

    maasser_user_db = MaasserUserDatabase()
    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        await send_message("MASR: welcome text", update, context)
        await send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    await send_message("MASR: fingeprint?", update, context)

    return MAASSER_EDIT_HANDLE


async def fun_maasser_edit_handle(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    query = get_message_text(update)

    maasser_user_db = MaasserUserDatabase()

    maasser_user = maasser_user_db.get(telegram_id)
    if maasser_user is None:
        await send_message("MASR: welcome text", update, context)
        await send_message("MASR: user not found", update, context)
        return MAASSER_PASSWORD_INIT

    maasser_user_db.remove_data(telegram_id, query)
    await send_message("MASR: removed", update, context)

    return MAASSER_NOMINAL
