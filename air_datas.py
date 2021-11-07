import requests
from pymongo import MongoClient, collection
import json
connection = MongoClient(host='127.0.0.1',port=27017)
db = connection.air
collection = db['datas']
collection2 = db['lists']
lists = {}
aqi = []
lat_long = []
sitename = []
url = "https://data.epa.gov.tw/api/v1/aqx_p_432?api_key=d13817bf-3ace-403c-a65b-aec9d7f3f393"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
res = requests.get(url,headers=headers)
datas = json.loads(res.text)
collection.drop()
collection2.drop()
for i in datas['records']:
    collection.insert([i])
    aqi.append(int(i['AQI']))
    lat_long.append([float(i['Latitude']),float(i['Longitude'])])
    sitename.append(i['SiteName'])
    print(i)
lists['SiteName']=sitename
lists['AQI']=aqi
lists['lat_long']=lat_long
collection2.insert([lists])