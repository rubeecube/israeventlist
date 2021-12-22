import json

from Localization import localize
from babel.dates import format_date, format_datetime, format_time

from Database.POIDatabase import POIDatabase

class Unit:
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

    @staticmethod
    def id_to_str(id, lang, inline=False):
        raise NotImplementedError


class Event (Unit):
    attr = ['name', 'description', 'interest_id', 'poi_id', 'date_event', 'time_event', 'recurrence']

    @staticmethod
    def dict_to_str(event, lang, inline=False):
        if inline:
            sep = " | "
        else:
            sep = "\n"
        s = event['name']
        if event['description'] is not None:
            s += ": " + event['description']
        s += sep
        if event['recurrence'] is not None and len(event['recurrence']) > 0:
            s += localize('every', lang) + ": " + ", ".join(event['recurrence'])
        else:
            s += format_date(event['date_event'], locale=lang)
        if event['time_event'] is not None:
            s += ' ' + localize('at', lang) + ' ' + format_time(event['time_event'], locale=lang)
        s += sep
        s += localize('poi', lang) + ': ' + POI.id_to_str(event['poi_id'], lang, inline=True)
        return s

    def to_str(self, lang, inline=False):
        if inline:
            sep = " | "
        else:
            sep = "\n"
        s = self.name
        if self.description is not None:
            s += ": " + self.description
        s += sep
        if self.recurrence is not None and len(self.recurrence) > 0:
            s += localize('every', lang) + ": " + ", ".join(self.recurrence)
        else:
            s += format_date(self.date_event, locale=lang)
        if self.time_event is not None:
            s += ' ' + localize('at', lang) + ' ' + format_time(self.time_event, locale=lang)
        s += sep
        s += localize('poi', lang) + ': ' + POI.id_to_str(self.poi_id, lang, inline=True)
        return s


class POI (Unit):
    attr = ['name', 'description', 'latitude', 'longitude', 'address', 'interest_id']

    @staticmethod
    def dict_to_str(poi, lang, inline=False):
        if inline:
            sep = " | "
        else:
            sep = "\n"
        s = poi['name']
        s += sep
        s += poi['address']
        return s

    def to_str(self, lang, inline=False):
        if inline:
            sep = " | "
        else:
            sep = "\n"
        s = self.name + ": " + self.description
        s += sep
        s += self.address
        return s

    @staticmethod
    def id_to_str(id, lang, inline=False):
        poi_database = POIDatabase()
        poi = poi_database.get_by_id(id)
        return POI.dict_to_str(poi, lang, inline)


class User(Unit):
    attr = ['telegram_id', 'phone', 'location', 'user_data', 'interests', 'misc']


class Interest(Unit):
    attr = ['name', 'id_parent', 'type_interest']