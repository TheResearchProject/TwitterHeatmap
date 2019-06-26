from __future__ import absolute_import, print_function

import tweepy
import json
import folium
from folium import plugins
import time
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver

# Create Map to display locations
m = folium.Map(location=[34.0522, -118.2437], zoom_start=10)
m.save('map.html')
print("Map generated")

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

# Read data from csv and add to heatmap
def HeatMap():
    df = pd.read_csv('data.csv')
    arr = df[['latitude', 'longitude']].as_matrix()
    m.add_child(plugins.HeatMap(arr, radius=15))
    m.save('map.html')

with open('data.csv', mode='a') as csv_file:
    fieldnames = ['latitude', 'longitude', 'date_created']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

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
                    datajson = json.loads(data)
                    created_at = datajson["created_at"]

                    # Longitude first, then latitude
                    coordinates = datajson["coordinates"]["coordinates"]
                    if(coordinates):
                        writer.writerow({'latitude': coordinates[1], 'longitude': coordinates[0], 'date_created': created_at})
                        print(coordinates[1], coordinates[0])
                        HeatMap()
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

print("Done collecting data")
HeatMap()