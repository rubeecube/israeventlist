from internals_admin import *
from StateManagement_admin import *
from ReplyMarkupHelper import ReplyMarkupHelper
from Database.InterestDatabase import InterestDatabase
from Unit import Interest


def funa_handle_add_interest(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyMarkupHelper.interests_build_reply_markup(
        show_level2=False,
        add_begin_button=[(localize("no parent interest", get_lang(update)), "**NOPARENT**")]
    )

    send_message('interest for add', update, context, reply_markup=reply_markup)

    return INTEREST_ADD_PARENT


def funa_handle_interest_add_parent(update: Update, context: CallbackContext) -> int:
    id_parent = get_message_text(update)

    interest_db = InterestDatabase()
    interests, parents = interest_db.get()

    if id_parent == "**NOPARENT**":
        id_parent = None
    elif int(id_parent) not in interests.keys():
        send_message('error', update, context)
        return AUTHENTICATED

    context.chat_data['INTEREST_ADD_id_parent'] = id_parent

    edit_message('saved', update, context)

    send_message('name of interest', update, context)

    return INTEREST_ADD_NAME


def funa_interest_add_name(update: Update, context: CallbackContext) -> int:
    message = get_message_text(update)

    context.chat_data['INTEREST_ADD_name'] = message

    interest = Interest()
    interest.name = context.chat_data['INTEREST_ADD_name']
    interest.id_parent = context.chat_data['INTEREST_ADD_id_parent']

    context.chat_data.pop("INTEREST_ADD_name")
    context.chat_data.pop("INTEREST_ADD_id_parent")

    interest_database = InterestDatabase()
    interest_database.save(interest)

    send_message('saved', update, context)

    return AUTHENTICATED
