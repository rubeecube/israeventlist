import sqlite3
import Database
from Unit import Interest


class InterestDatabase(Database.DatabaseHelper):
    def initialize(self):
        self.table_name = 'interests'
        self.table_schema = '''
            CREATE TABLE %s (
               id               INTEGER     PRIMARY KEY     AUTOINCREMENT,
               name             TEXT        NOT NULL,
               id_parent        INTEGER,
               type_interest    TEXT
            );'''

    def get_all(self):
        res = {}
        parents = {}
        query = self.cur.execute('''SELECT * FROM interests;''')
        for (identity, name, id_parent, type_interest) in query.fetchall():
            res[identity] = {
                "id": identity,
                "name": name,
                "id_parent": id_parent,
                "type_interest": type_interest
            }
            if id_parent is not None:
                if id_parent not in parents.keys():
                    parents[id_parent] = []
                parents[id_parent] += [{
                    "id": identity,
                    "name": name,
                    "id_parent": id_parent,
                    "type_interest": type_interest
                }]

        InterestDatabase.TEMP_DB = res, parents

        return res, parents

    def save(self, interest: Interest):
        row = self.cur.execute('''INSERT INTO interests
         (name, id_parent, type_interest) VALUES
         (?, ?, ?);''',
         (interest.name, interest.id_parent, interest.type_interest))

        self.con.commit()

        return interest
