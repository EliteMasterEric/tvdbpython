#!/usr/bin/env python3
"""Here's how you get information about a show.
For this one, you can type in the name of the show you want,
or replace show_name with a string.
"""
# Pull authentication from the auth example (see auth.py)
import time
from auth import authenticate
from helpers import get_input, ignore_unicode

def get_show(client):
    """Get information about a television show."""
    #show_name = "Adventure Time"
    show_name = get_input("Enter a show name: ")
    
    series = client.get_series(name=show_name)
    print(ignore_unicode(series.seriesName) + " (%s/10) (%s)"
        % (ignore_unicode(series.siteRating), ignore_unicode(series.id)))
    print(ignore_unicode(series.overview))
    print(series.banner)
    """
    count = 0
    for i in series.episodes:
        count += 1
        print("S%sE%s: %s (%s)" % (i.airedSeason, i.airedEpisodeNumber,
            ignore_unicode(i.episodeName), i.firstAired))
        print("    "+ignore_unicode(i.overview))
        time.sleep(1)
    print("TOTAL EPISODE COUNT: %s" % count)
    """
    

# If you want to run this as a standalone script
if __name__ == "__main__":
    print("Starting...")
    client = authenticate()
    get_show(client)