#coding=utf8
"""A Python library to perform operations using TheTVDB.com."""
import json
import requests
import xml.etree.ElementTree
#from .tvdb.models.series import Series
#from .tvdb.models.episode import Episode
#from .helpers.error import TVDBClientError
from tvdb.models.series import Series
from tvdb.models.episode import Episode
#from .helpers.error import TVDBClientError

# Temporary line for testing from source.
import sys
sys.path.append("E:/tvdbpython-master/tvdbpython/helpers/")
from error import TVDBClientError

__author__ = "EliteMasterEric"
__credits__ = ["EliteMasterEric", "TheTVDB"]
__license__ = "GNU GPL v3"
__version__ = "0.1"
__maintainer__ = "EliteMasterEric"
__email__ = "elitemastereric@gmail.com"
__status__ = "Development"

"""The website to base requsests on."""
TVDB_URL_BASE = "https://api-beta.thetvdb.com/"

class TVDBClient(object):
    """A Python API to perform operations using TheTVDB.com.
    Create an instance of this object, providing an API key,
    and a username and password if necessary.
    """

    """List of languages, with names and abbreviations tied to the IDs."""
    languages = { 0: { "name": "All Languages", "englishName": "All Languages", "abbreviation": "all" } }
    """Client's password, matching the given API key."""
    account_password = None
    """Client's usernamen, matching the given API key."""
    account_username = None
    """Client's session token, retrieved with the given API key and account."""
    account_session_token = None
    """Client's API key, matching the given account."""
    account_api_key = None
    
    def __init__(self, api_key, username=None, password=None):
        """Initialize the TVDBClient.
        You can choose to provide a username and password,
        which are required for operations like ratings or favorites
        but are not required for other operations.
        :param api_key: The application's API key.
        :param username: The user's username.
        :param password: The user's password.
        """
        if api_key is None:
            raise TypeError("An API key must be provided")
        else:
            self.account_api_key = api_key
            
        if username is not None and password is not None:
            self.account_username = username
            self.account_password = password
        elif username is not None and password is None:
            raise TypeError("The username was specified without a password")
        elif password is not None and username is None:
            raise TypeError("The password was specified without a username")

        self.login()
        
    def get_api_key(self):
        """Return the TVDBClient's API key."""
        return self.account_api_key
        
    def get_account_username(self):
        """Return the TVDBClient's account username."""
        return self.account_username
    
    def get_account_password(self):
        """Return the TVDBClient's account password."""
        return self.account_password
    
    def build_headers(self, key, lang):
        """Build a header object for the retrieve() method.
        You should not need to run this method yourself,
        as it is automatically run by retrieve().
        :param key: Whether to send the session token. Defaults to True.
        """
        headers = { }
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        
        if key:
            headers["Authorization"] = "Bearer " + self.account_session_token
            
        if lang:
            if lang is 0:
                raise TVDBClientError("'all' language currently not supported, "
                    "please specify a language.")
            else:
                headers["Accept-Language"] = self.languages[current_language]["abbreviation"]
               
        return headers
    
    def retrieve(self, method, route, data=None, key=True, lang=False, login=False):
        """Return data for the given method and route.
        :param method: Whether to use GET, POST, etc.
        :param key: Whether to send the session token. Defaults to True.
        :param lang: The desired language, as the language ID. Defaults to None.
        """
        # Convert the method argument from "GET" to requests.get() etc.
        method_to_call = getattr(requests, method.lower())
        header = self.build_headers(key, lang)
        url = TVDB_URL_BASE + route
        
        jsondata = json.dumps(data)
        
        # Actually perform the request
        if method.lower() in ("delete", "get"):
            response = method_to_call(url, headers=header,
                params=data, data=jsondata)
        else:
            response = method_to_call(url, headers=header,
                data=jsondata)
            
        if response.status_code == 200:
            # Parse the response as JSON and return it.
            return response.json()
        elif response.status_code == 401:
            # Login then try again.
            if login:
                raise TVDBClientError("Credentials invalid."
                    +str(data))
            else:
                print("Session token expired, retrieving new token"
                    "(401 error).")
                self.login()
                return self.retrieve(method, route, data, key)
        elif response.status_code == 404:
            raise TVDBClientError("Missing information or invalid method"
                "(404 error).")
        elif response.status_code == 409:
            raise TVDBClientError("A conflict prevented the record from"
                "being updated (409 error).")
        elif response.status_code == 405:
            raise TVDBClientError("Method not allowed (405 error)."
                +response.url)
        else:
            print(response.text)
            raise TVDBClientError("Unknown response code (%s error)." %
                (response.status_code))
    
    def login(self):
        """Retrieve a valid session token using API key, username, and pass.
        You should not need to run this method yourself,
        as it is automatically run by __init__().
        """
        if self.account_username is None or self.account_password is None:
            login_data = self.retrieve("POST", "login", data={
                "apikey": self.account_api_key
                    }, key=False, lang=False, login=True)
        else:
            login_data = self.retrieve("POST", "login", data={
                "apikey": self.account_api_key,
                "username": self.account_username, 
                "userpass": self.account_password
                    }, key=False, lang=False, login=True)
        
        self.account_session_token = login_data["token"]
        
        self.get_languages()
        
    def refresh_token(self):
        """Retrieve a valid session token based on an existing session token.
        You should not need to run this method yourself,
        as it is automatically run by retrieve().
        """
        data = self.retrieve("POST", "refresh_token")
        self.account_session_token = data.token
        
    def get_languages(self):
        """Retrieve the list of valid languages for TheTVDB.
        You should not need to run this method yourself,
        as it is automatically run by login().
        """
        data = self.retrieve("GET", "languages", lang=False)
        
        for i in data["data"]:
            self.languages[i["id"]] = {
                "name": i["name"],
                "englishName": i["englishName"],
                "abbreviation": i["abbreviation"]
            }
            if i["name"] is "English":
                self.current_language = i["id"]
        
    def get_series(self, name=None, imdbId=None, zap2itId=None):
        """Retrieve a Series object given its name, IMDB ID, or Zap2It ID.
        Each paramater is optional, but you must specify only one.
        :param name: The series' name, in string format.
        :param imdbId: The series' ID obtained from the IMDB website.
        :param zap2itId: The series' ID obtained from the Zap2It website.
        """
        # Note that since the search provides less information than
        # the full information given by accessing the series,
        # I search to get the seriesId then get the actual show information.
        if name is None and imdbId is None and zap2itId is None:
            raise TVDBClientError("You must specify a Series Name, IMDB ID,"
                "or Zap2It ID.")
        else:
            data = {"name": name, "imdbId": imdbId, "zap2itId": zap2itId}
            show = self.retrieve("GET", "search/series", data=data)
            series = self.retrieve("GET", "series/"+str(show["data"][0]["id"]))
            return Series(series["data"], tvdb_session=self)
                
    def get_user(self):
        """Retrieve a User object based on the currently authenticated user.
        If a username and password were not specified
        when creating the client, an error will be raised.
        """
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        user = self.retrieve("GET", "user")
        return User(user, tvdb_session=self)
            
    def add_favorite(self, id):
        """Add a series to the current user's favorites.
        :param id: The series' TVDB ID.
        """
        if id is None:
            raise TVDBClientError("You must specify the series ID"
                "for a favorite to add.")
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("PUT", "user/favorites/"+id)
            
    def remove_favorite(self, id):
        """Remove a series from the current user's favorites.
        :param id: The series' TVDB ID.
        """
        if id is None:
            raise TVDBClientError("You must specify the series ID"
                "for a favorite to remove.")
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("DELETE", "user/favorites/"+id)

    def get_ratings(self):
        """Retrieve the current user's ratings.
        Returns an array of Rating objects.
        :param id: The series' TVDB ID.
        """
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("GET", "user/ratings"+id)
        return Rating(data, tvdb_session=self)
        
    def add_series_rating(self, id, rating):
        """Add the given rating to the given series.
        Returns a Rating object representing the new rating.
        :param id: The series' TVDB ID.
        :param rating: The desired rating for the series, from 1 to 5.
        """
        if id is None:
            raise TVDBClientError("You must specify the series ID"
                "for a rating to add.")
        if rating is None or rating > 5 or rating < 1:
            raise TVDBClientError("You must specify a valid rating.")
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("PUT", "user/ratings/series/"+id+"/"+rating)
        return Rating(data, tvdb_session=self)
        
    def remove_series_rating(self, id):
        """Remove the user's rating for the given series.
        Returns an empty Rating object for consistency.
        :param id: The series' TVDB ID.
        """
        if id is None:
            raise TVDBClientError("You must specify the series ID"
                "for a rating to remove.")
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("DELETE", "user/ratings/series/"+id)
        return Rating(data, tvdb_session=self)
        
    def add_episode_rating(self, id, rating):
        """Add the given rating to the given episode.
        Returns a Rating object representing the new rating.
        :param id: The episode's TVDB ID.
        :param rating: The desired rating for the episode, from 1 to 5.
        """
        if id is None:
            raise TVDBClientError("You must specify the episode ID"
                "for a rating to add.")
        if rating is None or rating > 5 or rating < 1:
            raise TVDBClientError("You must specify a valid rating.")
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("PUT", "user/ratings/episode/%s"+id+"/"+rating)
        return Rating(data, tvdb_session=self)
        
    def remove_episode_rating(self, id):
        """Remove the user's rating for the given episode.
        Returns an empty Rating object for consistency.
        :param id: The episode's TVDB ID.
        """
        if id is None:
            raise TVDBClientError("You must specify the episode ID"
                "for a rating to remove.")
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("DELETE", "user/ratings/episode/"+id)
        return Rating(data, tvdb_session=self)
        
    def add_image_rating(self, id, rating):
        """Add the given rating to the given image.
        Returns a Rating object representing the new rating.
        :param id: The image's TVDB ID.
        :param rating: The desired rating for the image, from 1 to 5.
        """
        if id is None:
            raise TVDBClientError("You must specify the image ID"
                "for a rating to add.")
        if rating is None or rating > 5 or rating < 1:
            raise TVDBClientError("You must specify a valid rating.")
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("PUT", "user/ratings/image/"+id+"/"+rating)
        return Rating(data, tvdb_session=self)
        
    def remove_image_rating(self, id):
        """Remove the user's rating for the given image.
        Returns an empty Rating object for consistency.
        :param id: The image's TVDB ID.
        """
        if id is None:
            raise TVDBClientError("You must specify the image ID"
                "for a rating to remove.")
        if self.account_username is None or self.account_password is None:
            raise TVDBClientError("You must specify a valid"
                "username and password.")
        data = self.retrieve("DELETE", "user/ratings/image/"+id)
        return Rating(data, tvdb_session=self)
        
    def get_updated_series(self, fromTime, toTime=None):
        """Get a list of shows that have updated since the given time.
        You can specify a toTime to create a date range.
        :param fromTime: The epoch time to start your date range.
        :param toTime: The epoch time to end your date range.
        """