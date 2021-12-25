import json
import sqlite3
import Database


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

    def save(self, user):
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
            row = self.cur.execute(
                'INSERT INTO  %s' 
                ' (user_data, misc, interests, phone, location, telegram_id)'
                ' VALUES (?, ?, ?, ?, ?, ?);' % self.table_name,
                (user_data, misc, interests, user.phone, user.location, user.telegram_id)
            )

        except sqlite3.IntegrityError:
            row = self.cur.execute(
                'UPDATE %s'
                ' SET'
                ' user_data = ?, misc = ?, interests = ?, phone = ?, location = ?'
                ' WHERE telegram_id = ?;' % self.table_name,
                (user_data, misc, interests, user.phone, user.location, user.telegram_id)
            )

        self.con.commit()

        if row:
            return user
        else:
            return None

    def get(self, telegram_id=None):
        from Unit import User
        rows = self.cur.execute("SELECT * FROM %s WHERE telegram_id = ?;" % self.table_name, (str(telegram_id), ))

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
