"""These functions have nothing to do with the API, they just help ease
issues between Python 2 and 3.
"""
import unicodedata

def get_input(string):
    """Get input from console regardless of Python 2 or 3"""
    try:
        return raw_input(string)
    except:
        return input(string)

def get_config():
    """Create a config parser for reading INI files."""
    try:
        import ConfigParser
        return ConfigParser.ConfigParser()
    except:
        import configparser
        return configparser.ConfigParser()
        
def ignore_unicode(string):
    return str(string).encode('cp437', 'ignore').decode('utf-8', 'ignore')