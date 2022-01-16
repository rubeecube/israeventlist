import sqlite3
import os

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


class Database:
    con = None
    cur = None
    path = 'Storage/IsraEventList.db'

    def __init__(self, path='Storage/IsraEventList.db'):
        self.con = sqlite3.connect(os.path.abspath(self.path))
        self.cur = self.con.cursor()


class DatabaseHelper:
    db = None
    con = None
    cur = None

    TEMP_DB = None
    table_name = None
    table_schema = None

    def __init__(self):
        self.db = Database()
        self.con = self.db.con
        self.cur = self.db.con.cursor()
        self.initialize()
        self.post_initialize()

    def initialize(self):
        raise NotImplementedError

    def post_initialize(self):
        try:
            self.cur.execute("SELECT * FROM %s;", self.table_name)
        except sqlite3.OperationalError:
            try:
                self.cur.execute(self.table_schema % self.table_name)
                self.con.commit()
            except sqlite3.OperationalError:
                pass

    def get(self, **kwargs):
        raise NotImplementedError
