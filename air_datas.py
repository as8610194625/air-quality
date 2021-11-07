import requests
from pymongo import MongoClient, collection
import json
connection = MongoClient(host='127.0.0.1',port=27017)
db = connection.air
collection = db['datas']
url = "https://data.epa.gov.tw/api/v1/aqx_p_432?api_key=d13817bf-3ace-403c-a65b-aec9d7f3f393"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
res = requests.get(url,headers=headers)
datas = json.loads(res.text)
collection.drop()
for i in datas['records']:
    collection.insert([i])
    print(i)
