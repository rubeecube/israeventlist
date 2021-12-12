import sqlite3
from Database import Database
from Unit import POI


class POIDatabase:

    POIs = None

    def __init__(self):
        self.db = Database()
        self.con = self.db.con
        self.cur = self.db.con.cursor()
        self.initialize()

    def initialize(self):
        try:
            self.cur.execute('''SELECT * FROM poi;''')
        except sqlite3.OperationalError:
            self.cur.execute('''
            CREATE TABLE poi (
               id               INTEGER     PRIMARY KEY     AUTOINCREMENT,
               name             TEXT        NOT NULL,
               description      TEXT,
               location         TEXT,
               address          TEXT,
               interest_id      INTEGER
            );''')

            self.con.commit()

    def get_pois(self):
        if POIDatabase.POIs is not None:
            return POIDatabase.POIs

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

        POIDatabase.POIs = res

        return res

    def save_poi(self, poi: POI):
        row = self.cur.execute('''INSERT INTO poi
         (name, description, location, address, interest_id) VALUES
         (?, ?, ?, ?, ?);''',
         (poi.name, poi.description, poi.location, poi.address, poi.interest_id))

        self.con.commit()

        return poi
