from Database import DatabaseHelper
from Database.MaasserUserDatabase import MaasserUserDatabase


class Unit:
    database_class = DatabaseHelper
    attr = None

    def __init__(self):
        for attr in self.attr:
            object.__setattr__(self, attr, None)

    def __setattr__(self, key, value):
        if self.attr is not None and key in self.attr:
            object.__setattr__(self, key, value)
        else:
            raise AttributeError

    def __getattr__(self, key):
        if self.attr is not None and key in self.attr:
            return object.__getattribute__(self, key)
        else:
            raise AttributeError

    def to_str(self, lang, inline=False):
        return str(self)

    @classmethod
    def id_to_str(cls, element_id, lang, inline=False):
        database = cls.database_class()
        element = database.get(element_id=element_id)
        return cls.dict_to_str(element, lang, inline)


class MaasserUser(Unit):
    database_class = MaasserUserDatabase
    attr = ['telegram_id', 'percentage', 'currency', 'public_key', 'encrypted_private_key', 'encrypted_data']
