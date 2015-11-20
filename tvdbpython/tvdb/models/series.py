from .episode import Episode

class Series(object):
    # See the API for the available attributes.
    def __init__(self, *initial_data, **kwargs):
        """Create the series object."""
        from client import TVDBClient
        self.tvdb_session = kwargs["tvdb_session"]
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    @property
    def episodes(self):
        """A property to get the episodes of a series."""
        data = self.tvdb_session.retrieve("GET", "series/%s/episodes" % self.id)
        
        page = 1
        while page <= data["links"]["last"]:
            if page is 1:
                for i in data["data"]:
                    yield Episode(i)
            else:
                data = self.tvdb_session.retrieve("GET", "series/%s/episodes" % self.id, data={"page":page})
                for i in data["data"]:
                    yield Episode(i)
            page += 1