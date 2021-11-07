from pymongo import MongoClient, collection
import json

connection = MongoClient(host='127.0.0.1',port=27017)
db = connection.air
collection = db['datas']
datas = collection.find()
for i in datas:
    print(i['SiteName'],i['AQI'])