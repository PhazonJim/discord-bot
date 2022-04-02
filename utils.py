import json
import os

CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache.json")

def loadCache():
    cache = {}
    try:
        with open(CACHE_FILE, "r") as fin:
            cache = json.load(fin)
    except Exception as e:
        print (e)
    return cache

def saveCache(cache):
    with open(CACHE_FILE, "w") as fout:
        for chunk in json.JSONEncoder().iterencode(cache):
            fout.write(chunk)