class Episode(object):
    # See the API for the available attributes.
    def __init__(self, *initial_data, **kwargs):
        """Create the episode object."""
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
