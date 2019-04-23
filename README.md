# TweetCollector
This is a python application that scrapes tweets from a geotagged location (in this case a box around the Los Angeles area) and stores them into a local database using Mongodb

## Usage
Assuming you have Mongodb installed and running locally, just run
```
python main.py
```
This should begin the script and begin scraping tweets and display the timestamp.

TODO:
- Fix script runtime
- Display tweets onto heatmap using Folium
- Make geocode modular
