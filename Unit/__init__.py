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


class Event (Unit):
    attr = ['name', 'description', 'location', 'address', 'interest_id', 'poi_id']


class POI (Unit):
    attr = ['name', 'description', 'location', 'address', 'interest_id']


class User(Unit):
    attr = ['telegram_id', 'phone', 'location', 'user_data', 'interests', 'misc']
