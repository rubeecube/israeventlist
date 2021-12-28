from admin import main as admin_main
from user import main as user_main

if __name__ == '__main__':
    updater_admin = admin_main()
    updater_user = user_main()

    updater_admin.idle()
    updater_user.idle()
