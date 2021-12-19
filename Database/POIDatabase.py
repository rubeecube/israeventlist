import sqlite3
import Database
from Unit import POI


class POIDatabase(Database.DatabaseHelper):
    def initialize(self):
        self.table_name = 'poi'
        self.table_schema = '''
        CREATE TABLE %s (
               id               INTEGER     PRIMARY KEY     AUTOINCREMENT,
               name             TEXT        NOT NULL,
               description      TEXT,
               location         TEXT,
               address          TEXT,
               interest_id      INTEGER
            );
        '''

    def get_all(self):
        res = {}
        query = self.cur.execute('''SELECT * FROM poi;''')
        for (identity, name, description, location, address, interest_id) in query.fetchall():
            res[identity] = {
                "id": identity,
                "name": name,
                "description": description,
                "location": location,
                "address": address,
                "interest_id": interest_id
            }

        POIDatabase.TEMP_DB = res

        return res

    def save(self, poi: POI):
        row = self.cur.execute('''INSERT INTO poi
         (name, description, location, address, interest_id) VALUES
         (?, ?, ?, ?, ?);''',
         (poi.name, poi.description, poi.location, poi.address, poi.interest_id))

        self.con.commit()

        return poi
