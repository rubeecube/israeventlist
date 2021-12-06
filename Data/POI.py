class POI:
    name = None
    description = None
    location = None
    address = None
    interest_id = None

    def __setattr__(self, key, value):
        if key in ['name', 'description', 'location', 'address', 'interest_id']:
            object.__setattr__(self, key, value)
        else:
            raise AttributeError

    def __getattr__(self, key):
        if key in ['name', 'description', 'location', 'address', 'interest_id']:
            return object.__getattr__(self, key)
        else:
            raise AttributeError
