from internals import *
from StateManagement import *
from ReplyMarkupHelper import ReplyMarkupHelper
from Globals import Globals


def fun_ask_interests(update: Update, context: CallbackContext) -> int:
    interests = get_interests(update, context)

    reply_markup = ReplyMarkupHelper.interests_build_reply_markup(
        interests,
        add_end_button=[(localize('finish', 'fr'), "***END***")]
    )

    send_message('retrieve interests', update, context, reply_markup=reply_markup)

    return HANDLE_INTERESTS


def fun_handle_interests(update: Update, context: CallbackContext) -> int:
    chosen_data = []
    message = update.callback_query.message

    for inlinekb in message['reply_markup']['inline_keyboard']:
        if len(inlinekb) > 1 and inlinekb[1]['text'] == Globals.EMOJI_CHECKED:
            chosen_data += [inlinekb[1]['callback_data']]

    if update.callback_query.data == "***END***":
        save_interests(update, context, chosen_data)

        context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                              message_id=update.callback_query.message.message_id,
                                              inline_message_id=update.callback_query.inline_message_id,
                                              reply_markup=ReplyMarkupHelper.interests_build_reply_markup(
                                                  chosen_data,
                                                  only_selected=True
                                              )
                                              )

        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=localize('thanks interests', 'fr'))

        context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                 text=localize("command list", get_lang(update)),
                                 reply_markup=get_commands(get_lang(update), exclude=["/stop"]))

        return NOMINAL

    if update.callback_query.data in chosen_data:
        chosen_data.remove(update.callback_query.data)
    else:
        chosen_data += [update.callback_query.data]

    context.bot.edit_message_reply_markup(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        inline_message_id=update.callback_query.inline_message_id,
        reply_markup=ReplyMarkupHelper.interests_build_reply_markup(
            chosen_data,
            add_end_button=[(localize('finish', get_lang(update)), "***END***")]
        )
    )
    return HANDLE_INTERESTS
