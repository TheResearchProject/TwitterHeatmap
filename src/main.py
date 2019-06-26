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
import threading

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
    m = folium.Map(location=[34.0522, -118.2437], zoom_start=8)
    m.save('map.html')
    print("Map generated")
    df = pd.read_csv('data.csv')
    arr = df[['latitude', 'longitude']].values
    m.add_child(plugins.HeatMap(arr, radius=15))
    m.save('map.html')

# Function to run a function for a certain amount of time
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

# Refresh heatmap every x seconds
x = 10
set_interval(HeatMap, x)

with open('data.csv', mode='a') as csv_file:
    fieldnames = ['latitude', 'longitude', 'date_created']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    class StreamListener(tweepy.StreamListener):
        def __init__(self):
            super(StreamListener, self).__init__()

        def on_connect(self):
            print("Connected to streaming API")

        def on_data(self, data):
            try:
                # Get data from tweet
                datajson = json.loads(data)
                created_at = datajson["created_at"]

                # Longitude first, then latitude
                if(datajson["coordinates"]):
                    # Coordinates from tweet
                    coordinates = datajson["coordinates"]["coordinates"]
                    latitude = coordinates[1]
                    longitude = coordinates[0]

                    # Check if latitude and longitude are floats
                    if(isinstance(latitude, float) and isinstance(longitude, float)):
                        # Write to csv file
                        writer.writerow({'latitude': latitude, 'longitude': longitude, 'date_created': created_at})
                        print(latitude, longitude)
                return True
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
    GEOBOX_LA = [-119.2279,33.4263,-116.8997,34.7189]
    sapi = tweepy.streaming.Stream(auth, StreamListener()) 
    sapi.filter(locations=GEOBOX_LA)

print("Stream stopped")