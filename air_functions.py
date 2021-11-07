from pymongo import MongoClient, collection
from math import dist, floor
import numpy as np
connection = MongoClient(host='127.0.0.1',port=27017)
db = connection.air
collection = db['lists']
datas = list(collection.find())[0]
aqi = datas['AQI']
sitename = datas['SiteName']
lat_long = np.matrix(datas['lat_long'])
# print(datas['lat_long'])
# print(lat_long)
def np_getDistance(A , B ):# [[lat,long]]先緯度後經度
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = 0.003353 # Partial rate of the earth
    # change angle to radians
    radLatA = np.radians(A[:,0])
    radLonA = np.radians(A[:,1])
    radLatB = np.radians(B[:,0])
    radLonB = np.radians(B[:,1])
    pA = np.arctan(rb / ra * np.tan(radLatA))
    pB = np.arctan(rb / ra * np.tan(radLatB))
    
    x = np.arccos( np.multiply(np.sin(pA),np.sin(pB)) + np.multiply(np.multiply(np.cos(pA),np.cos(pB)),np.cos(radLonA - radLonB)))
    c1 = np.multiply((np.sin(x) - x) , np.power((np.sin(pA) + np.sin(pB)),2)) / np.power(np.cos(x / 2),2)
    c2 = np.multiply((np.sin(x) + x) , np.power((np.sin(pA) - np.sin(pB)),2)) / np.power(np.sin(x / 2),2)
    dr = flatten / 8 * (c1 - c2)
    distance = 0.001 * ra * (x + dr)
    return distance
# find_loc = np.matrix([[25.038279754851253,121.49910795854528]])
# 距縣市距離(全部)
def air_aqi(location):
    disALL = np_getDistance(lat_long,np.matrix(location))
    disAll_sort = np.argsort(disALL,axis=0) #index由小排到大
    aqi_site1 = aqi[int(disAll_sort[0,0])]
    aqi_site2 = aqi[int(disAll_sort[1,0])]
    aqi_site3 = aqi[int(disAll_sort[2,0])]
    disMinName1 = sitename[int(disAll_sort[0,0])]
    disMinName2 = sitename[int(disAll_sort[1,0])]
    disMinName3 = sitename[int(disAll_sort[2,0])]
    # print(disAll_sort)
    # print(aqi_site1,disMinName1)
    # print(aqi_site2,disMinName2)
    # print(aqi_site3,disMinName3)
    disALL.T.sort() #值由小排到大
    # print(disALL)
    d1 = disALL[0,0]
    d2 = disALL[1,0]
    d3 = disALL[2,0]
    distance = d1 + d2 + d3
    # print(distance)
    aqi_avg = (aqi_site1*d1+aqi_site2*d2+aqi_site3*d3)/distance
    print(aqi_avg)
    return aqi_avg
# air_aqi(find_loc)