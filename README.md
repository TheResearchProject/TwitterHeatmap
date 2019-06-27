# TweetCollector
This is a python application that scrapes tweets from a geotagged location (in this case near the Los Angeles area) and displays a heatmap where people are tweeting from. Note: OAuth authentication keys needed and read from a text file named "keys.txt"

## Screenshots
![alt text](https://github.com/sondr0p/TwitterHeatmap/blob/master/screenshots/california.png)
![alt text](https://github.com/sondr0p/TwitterHeatmap/blob/master/screenshots/socal.png)

## Requirements
- tweepy Twitter API to scrape tweets (https://www.tweepy.org/)
- folium to display map (https://python-visualization.github.io/folium/)
- pandas, matplotlib, and seaborn for data manipulation

## Usage
```
python main.py
```
This should begin the script and display the map in the html file. Console should display coordinates of scraped tweet, and if the map was refreshed

## TODO
- Ping the map when new tweet is collected
- Clean the data.csv so there aren't a lot of rows
