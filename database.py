import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

tdb = myclient["twitterdb"]
MONGO_HOST = 'mongodb://localhost/twitterdb'
print(myclient.list_database_names())