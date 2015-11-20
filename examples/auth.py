#!/usr/bin/env python3
"""Here's how you go about authenticating yourself! The important thing to
note here is that this script will be used in the other examples so
set up a test user with API credentials and set them up in auth.ini.
"""
# Temporary line for testing from source.
import sys
sys.path.append("E:/tvdbpython-master/tvdbpython")

from client import TVDBClient
#from tvdbpython import TVDBClient
from helpers import get_input, get_config

def authenticate():
    # Get client ID and secret from auth.ini
    config = get_config()
    config.read('auth.ini')
    username = config.get('credentials', 'username')
    password = config.get('credentials', 'password')
    api_key = config.get('credentials', 'api_key')
    print("Username: "+username)
    client = TVDBClient(api_key, username, password)

    return client

# If you want to run this as a standalone script, so be it!
if __name__ == "__main__":
    authenticate()