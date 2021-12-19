import json
import sqlite3
import Database
from Unit import User


class UserDatabase(Database.DatabaseHelper):
    def initialize(self):
        self.table_name = 'users'
        self.table_schema = '''
            CREATE TABLE %s (
               id               INTEGER     PRIMARY KEY     AUTOINCREMENT,
               user_data        TEXT        NOT NULL,
               misc             TEXT,
               interests        TEXT,
               phone            TEXT,
               location         TEXT,
               telegram_id      TEXT        UNIQUE
            );'''

    def save(self, user: User):
        user_data = None
        misc = None
        interests = None

        if user.user_data is not None:
            user_data = json.dumps(user.user_data)
        if user.misc is not None:
            misc = json.dumps(user.misc)
        if user.interests is not None:
            interests = json.dumps(user.interests)

        try:
            row = self.cur.execute('''INSERT INTO users
             (user_data, misc, interests, phone, location, telegram_id) VALUES
             (?, ?, ?, ?, ?, ?);''',
             (user_data, misc, interests, user.phone, user.location, user.telegram_id))

        except sqlite3.IntegrityError:
            row = self.cur.execute('''UPDATE users SET user_data = ?, misc = ?, interests = ?, phone = ?,
             location = ? WHERE telegram_id = ?;''',
                    (user_data, misc, interests, user.phone, user.location, user.telegram_id))

        self.con.commit()

        if row:
            return user
        else:
            return None

    def get(self, telegram_id):
        rows = self.cur.execute("SELECT * FROM users WHERE telegram_id = ?;", (str(telegram_id), ))

        row = rows.fetchone()

        if not row:
            return None

        user = User()

        row_id, user_data, misc, interests, phone, location, telegram_id = row

        if user_data is not None:
            user.user_data = json.loads(user_data)
        if misc is not None:
            user.misc = json.loads(misc)
        if interests is not None:
            user.interests = json.loads(interests)

        if phone is not None:
            user.phone = phone
        if location is not None:
            user.location = location
        if telegram_id is not None:
            user.telegram_id = telegram_id

        return user


