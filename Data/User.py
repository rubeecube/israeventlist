class User:
    telegram_id = None
    user_data = None
    misc = None
    interests = None
    phone = None
    location = None

    def __setattr__(self, key, value):
        if key in ['telegram_id', 'phone', 'location', 'user_data', 'interests', 'misc']:
            object.__setattr__(self, key, value)
        else:
            raise AttributeError

    def __getattr__(self, key):
        if key in ['telegram_id', 'phone', 'location', 'user_data', 'interests', 'misc']:
            return object.__getattr__(self, key)
        else:
            raise AttributeError
