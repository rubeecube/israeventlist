import datetime
import sqlite3
import Database
from Unit import Event
from dateutil import parser
import json


class EventDatabase(Database.DatabaseHelper):
    def initialize(self):
        self.table_name = 'event'
        self.table_schema = '''
        CREATE TABLE %s (
               id               INTEGER     PRIMARY KEY     AUTOINCREMENT,
               name             TEXT        NOT NULL,
               description      TEXT,
               interest_id      INTEGER,
               poi_id           INTEGER,
               date_event       TEXT,
               time_event       TEXT,
               recurrence       TEXT
            );
        '''

    def get_all(self, interest_id=None, poi_id=None):
        res = {}
        if interest_id is None and poi_id is None:
            query = self.cur.execute('''SELECT * FROM event;''')
        elif interest_id is None:
            query = self.cur.execute('''SELECT * FROM event WHERE poi_id = ?;''', (poi_id,))
        elif poi_id is None:
            query = self.cur.execute('''SELECT * FROM event WHERE interest_id = ?;''', (interest_id,))
        else:
            query = self.cur.execute('''SELECT * FROM event WHERE interest_id = ? AND poi_id = ?;''', (interest_id, poi_id))
        for (identity, name, description, interest_id, poi_id, date_event, time_event, recurrence) in query.fetchall():
            res[identity] = {
                "id": identity,
                "name": name,
                "description": description,
                "interest_id": interest_id,
                "poi_id": poi_id,
                "date_event": parser.parse(date_event + ' ' + time_event).date(),
                "time_event": parser.parse(date_event + ' ' + time_event).time(),
                "recurrence": json.loads(recurrence)
            }

        return res

    def save(self, event: Event):
        row = self.cur.execute('''INSERT INTO event
         (name, description, interest_id, poi_id, date_event, time_event, recurrence) VALUES
         (?, ?, ?, ?, ?, ?, ?);''',
         (event.name, event.description, event.interest_id, event.poi_id, event.date_event, event.time_event, event.recurrence))

        self.con.commit()

        return event

