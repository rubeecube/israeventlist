import sqlite3
import Database


class POIDatabase(Database.DatabaseHelper):
    def initialize(self):
        self.table_name = 'poi'
        self.table_schema = '''
        CREATE TABLE %s (
               id               INTEGER     PRIMARY KEY     AUTOINCREMENT,
               name             TEXT        NOT NULL,
               description      TEXT,
               latitude         TEXT,
               longitude        TEXT,
               address          TEXT,
               interest_id      INTEGER
            );
        '''

    def get_all(self, interest_id=None):
        res = {}
        if interest_id is None:
            query = self.cur.execute('''SELECT * FROM poi;''')
        else:
            query = self.cur.execute('''SELECT * FROM poi WHERE interest_id = ?;''', (interest_id,))
        for (identity, name, description, latitude, longitude, address, interest_id) in query.fetchall():
            res[identity] = {
                "id": identity,
                "name": name,
                "description": description,
                "latitude": latitude,
                "longitude": longitude,
                "address": address,
                "interest_id": interest_id
            }

        POIDatabase.TEMP_DB = res

        return res

    def get_by_id(self, id):
        res = {}
        query = self.cur.execute('''SELECT * FROM poi WHERE id = ?;''', (id,))
        for (identity, name, description, latitude, longitude, address, interest_id) in query.fetchall():
            res[identity] = {
                "id": identity,
                "name": name,
                "description": description,
                "latitude": latitude,
                "longitude": longitude,
                "address": address,
                "interest_id": interest_id
            }
        if len(res) == 0:
            return None
        return list(res.values())[0]

    def save(self, poi):
        row = self.cur.execute('''INSERT INTO poi
         (name, description, latitude, longitude, address, interest_id) VALUES
         (?, ?, ?, ?, ?);''',
         (poi.name, poi.description, poi.latitude, poi.longitude, poi.address, poi.interest_id))

        self.con.commit()

        return poi
