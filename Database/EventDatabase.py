import json

from dateutil import parser

import Database


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

    def get(self, element_id=None, interest_id=None, poi_id=None):
        res = {}
        if element_id is None and interest_id is None and poi_id is None:
            query = self.cur.execute('SELECT * FROM event;')
        else:
            query_l = []
            query_t = ()
            if element_id is not None:
                query_l += ['id = ?']
                query_t += (element_id,)
            if interest_id is not None:
                query_l += ['interest_id = ?']
                query_t += (interest_id,)
            if poi_id is not None:
                query_l += ['poi_id = ?']
                query_t += (poi_id,)

            query = self.cur.execute('SELECT * FROM event WHERE ' + ' AND '.join(query_l), query_t)

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

        if len(res) == 1 and element_id is not None:
            return list(res.values())[0]
        return res

    def save(self, event):
        row = self.cur.execute(
            'INSERT INTO event'
            ' (name, description, interest_id, poi_id, date_event, time_event, recurrence)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?);',
            (event.name, event.description, event.interest_id, event.poi_id, event.date_event, event.time_event,
             event.recurrence)
        )

        self.con.commit()

        return row
