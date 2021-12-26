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

    def get(self, element_id=None, interest_id=None):
        res = {}
        if element_id is None and interest_id is None:
            query = self.cur.execute('SELECT * FROM poi;')
        else:
            query_l = []
            query_t = ()
            if element_id is not None:
                query_l += ['id = ?']
                query_t += (element_id,)
            if interest_id is not None:
                query_l += ['interest_id = ?']
                query_t += (interest_id,)

            query = self.cur.execute('SELECT * FROM poi WHERE ' + ' AND '.join(query_l), query_t)

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

        if len(res) == 1 and element_id is not None:
            return list(res.values())[0]
        return res

    def save(self, poi):
        row = self.cur.execute(
            'INSERT INTO poi'
            ' (name, description, latitude, longitude, address, interest_id)'
            ' VALUES (?, ?, ?, ?, ?);',
            (poi.name, poi.description, poi.latitude, poi.longitude, poi.address, poi.interest_id)
        )

        self.con.commit()

        return row
