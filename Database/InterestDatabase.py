import Database


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

    def get(self, element_id=None, return_parents=True):
        res = {}
        parents = {}

        if element_id is None:
            query = self.cur.execute('SELECT * FROM interests;')
        else:
            query = self.cur.execute('SELECT * FROM interests WHERE id = ?;', (element_id,))

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

        if len(res) == 1 and element_id is not None:
            return list(res.values())[0]
        if return_parents:
            return res, parents
        return res

    def save(self, interest):
        row = self.cur.execute(
            'INSERT INTO interests'
            ' (name, id_parent, type_interest)'
            ' VALUES (?, ?, ?);',
            (interest.name, interest.id_parent, interest.type_interest)
        )

        self.con.commit()

        return row
