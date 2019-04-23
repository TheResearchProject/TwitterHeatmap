from __future__ import absolute_import, print_function

import tweepy
import json
from pymongo import MongoClient
import folium
import time
import sys

# Get authentication keys from file
f = open("keys.txt", "r")

# == OAuth Authentication ==
consumer_key = f.readline().rstrip()
consumer_secret = f.readline().rstrip()
access_token = f.readline().rstrip()
access_token_secret = f.readline().rstrip()

f.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

MONGO_HOST = 'mongodb://localhost:27017/'

class StreamListener(tweepy.StreamListener):
    def __init__(self, time_limit=20):
        self.start_time = time.time()
        self.limit = time_limit
        super(StreamListener, self).__init__()
    def on_connect(self):
        print("Connected to streaming API")
    def on_data(self, data):
        try:
            if (time.time() - self.start_time) < self.limit:
                client = MongoClient(MONGO_HOST)
                db = client.twitterdb
                datajson = json.loads(data)
                created_at = datajson["created_at"]
                print("Tweet collected at " + str(created_at))
                db.twitter_search.insert(datajson)
                return True
            else:
                print("Ending stream")
                return False
        except Exception as e:
            print(e)

    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return False
        # return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return False
        # return True # Don't kill the stream

# Streams tweets from box around Los Angeles, CA area
GEOBOX_LA = [-118.4737,33.9332,-118.0206,34.2039]
sapi = tweepy.streaming.Stream(auth, StreamListener()) 
sapi.filter(locations=GEOBOX_LA)


m = folium.Map(location=[20, 0], zoom_start=3.5)
m = folium.Map(location=[48.85, 2.35], tiles="Mapbox Control Room", zoom_start=2)
m.save('map.html')

