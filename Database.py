import sqlite3


class Database:
    con = None
    cur = None

    def __init__(self):
        self.con = sqlite3.connect('IsraEventList.db')
        self.cur = self.con.cursor()
