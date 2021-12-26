import os.path

from internals_admin import *
from StateManagement_admin import *
import uuid
import datetime
import os


def funa_handle_push(update: Update, context: CallbackContext) -> int:
    message = get_message(update)

    path = str(uuid.uuid5(uuid.NAMESPACE_URL, str(datetime.datetime.now().timestamp())))

    with open(os.path.join("path", path), "w+") as f:
        f.write(message)

    send_message('ok', update, context)

    return AUTHENTICATED
