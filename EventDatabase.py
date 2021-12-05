import sqlite3
from Database import Database


class EventDatabase:
    BASE_INTERESTS = {
        "Activités sportives": [
            "Football",
            "Paddle",
            "Squash",
            "Tennis",
            "Treks/Tiyulim"
        ],
        "Culture": [
            "Show",
            "Soirée",
            "Conférences",
            "Concerts",
        ],
        "Synagogues": [
            "Horaires",
            "Mikvé",
            "Activités",
            "Cours",
        ],
        "Literature": [
            "Nouveautés",
            "Dédicaces"
        ],
        "Liens externes": [
            "Sites utiles"
        ],
        "Boire/Manger": [
            "Restaurants",
            "Cafés",
            "Bars"
        ],
        "Shabbats organisés": [
            "Synagogues",
            "Chez l'habitant",
            "Traiteur",
            "Jeunes",
            "Celibataires",
        ],
        "Finances, Legal": [
            "Entre-aide",
            "Conseil",
            "Chroniques"
        ],
        "Activités ados (-13)": [
            "Treks/Tiyulim",
            "Colonies",
            "Talmud Thora"
            "Cours privés",
            "Musique",
            "Tsaaron"
        ]
    }

    INTERESTS = None

    def __init__(self):
        self.db = Database()
        self.con = self.db.con
        self.cur = self.db.con.cursor()
        self.initialize()

    def initialize(self):
        try:
            self.cur.execute('''SELECT * FROM interests;''')
        except sqlite3.OperationalError:
            self.cur.execute('''
            CREATE TABLE interests (
               id               INTEGER     PRIMARY KEY     AUTOINCREMENT,
               name             TEXT        NOT NULL,
               id_parent        INTEGER,
               type_interest    TEXT
            );''')

            for interest_level1 in sorted(EventDatabase.BASE_INTERESTS.keys()):
                row = self.cur.execute('''INSERT INTO interests (name) VALUES (?);''', (interest_level1,))
                parent_id = row.lastrowid
                for interest_level2 in sorted(EventDatabase.BASE_INTERESTS[interest_level1]):
                    self.cur.execute('''INSERT INTO interests (name, id_parent) VALUES (?, ?);''', (interest_level2,parent_id))

            self.con.commit()

    def get_interests(self):
        if EventDatabase.INTERESTS is not None:
            return EventDatabase.INTERESTS

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

        EventDatabase.INTERESTS = res, parents

        return res, parents


