# -*- coding: utf-8 -*-
"""!map <place> return a map of place. Optional "zoom" and "maptype" parameters are accepted."""
# example queries:
# !map new york city
# !map united states zoom=4
# !map united states zoom=4 maptype=satellite

from urllib import quote
import re

def makemap(query):
    querywords = []
    args = {
        "maptype": "roadmap",
    }
    for word in query.split(" "):
        if '=' in word:
            opt, val = word.split("=")
            args[opt] = val
        else:
            querywords.append(word)

    query = quote(" ".join(querywords))

    # Slack seems to ignore the size param
    #
    # To get google to auto-reasonably-zoom its map, you have to use a marker
    # instead of using a "center" parameter. I found that setting it to tiny
    # and grey makes it the least visible.
    url = "https://maps.googleapis.com/maps/api/staticmap?size=800x400&markers=size:tiny%7Ccolor:0xAAAAAA%7C{}&maptype={}"
    url = url.format(query, args["maptype"])

    if "zoom" in args:
        url += "&zoom={}".format(args["zoom"])

    return url

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!map (.*)", text)
    if not match: return

    return makemap(match[0])
