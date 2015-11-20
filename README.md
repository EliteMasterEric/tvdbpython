TVDBPython
===========

An unofficial Python client for [TheTVDB.com](http://thetvdb.com/). It can be used to
interact with the TVDB API in your projects, allowing you to, simply given a show's name,
retrieve information such as lists of actors or episode air dates.

This project is adapting as TheTVDB creates its new RESTful API.
The beta documentation can be found [here](https://api-beta.thetvdb.com/swagger).

You must [register](http://thetvdb.com/?tab=apiregister) your client with the TVDB API, and provide the api key to
make most requests to the API. See the [Programmer API](http://www.thetvdb.com/wiki/index.php/Programmers_API) page
for more information. 

This project and its structure are based heavily on [ImgurPython](https://www.github.com/Imgur/ImgurPython)

Requirements
------------

- Python >= 2.7
- [requests](http://docs.python-requests.org/en/latest/user/install/)

TVDB API Documentation
-----------------------

TVDB's API documentaiton can be found [here](http://www.thetvdb.com/wiki/index.php/Programmers_API).

Support
---------

For API support, please [submit an issue](https://github.com/Imgur/imgurpython/issues/).

Installation
------------

The project will be eventually available on [PyPI](), allowing for easy installation.
You can use pip or easy_install to install the library.

    pip install tvdbpython
    easy_install tvdbpython
    
Project Goals
------------

The TVDBPython library has several goals we attempt to follow during development.

* Simplicity
TVDBPython code should be easy to understand and use.
Method names should be self-explanatory, code should be kept clean
by following the [Google Style Guide](https://github.com/google/styleguide), and popular actions
should not be convoluted or hard to do.
    
* Documentation
TVDBPython code should be very well documented.
The code's docstrings (created/verified with doctest), the wikis,
and the README files should be easily read, easily navigated,
and provide sufficient, up-to-date information for all methods.
The docstrings are compliant with can be accessed by viewing the library's code,
or by running help(object) on any of the client's methods or objects.
    
* Openness
The TVDBPython library is available on GitHub under the GNU GPL v3 license.
All aspects of the library's code will remain open-source and fully accessible.
    
* Reduced Load
The TVDBPython library is designed to reduce bandwidth and data usage where possible.
Using generators, it should only retrieve data when requested, and also retrieve
compressed zip files, further reducing server load.
    
* Flexibility
TheTVDB is a changing platform, and new features can be added at any time.
TVDBPython is designed to be easily expanded, such that new methods or
features can be implemented easily, without destroying existing
projects or code.

Library Usage
------------

View examples of library usage on our [wiki]().