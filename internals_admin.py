from internals import *


def get_raw_commands_admin(lang="fr"):
    commands = []
    for command in ["add", "commands"]:
        commands += [
            ("/%s" % command, "%s" % localize("command_admin %s" % command, lang)),
        ]
    return commands


def get_commands_admin(lang="fr", exclude=None):
    button_list = []
    for command, desc in get_raw_commands_admin(lang):
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


