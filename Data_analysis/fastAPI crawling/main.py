import os
import pymongo
import subprocess
import datetime
import requests
import json

from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

#naver config
dbaddrs = 'localhost'
dbport = 27017

#검색 api 발급받아 사용
headers = {"X-Naver-Client-Id":"5DmpXXFcW1sFy6UwK8Kk", "X-Naver-Client-Secret":"4Na9VGgton"}
searchTargetCount = 100
naverUrl = "https://openapi.naver.com/v1/search/shop.json?display="+str(searchTargetCount)+'&query='

#http://127.0.0.1:8000
@app.get("/")
async def root():
    return {"message":"yundaehyuck"}

# @app.get("/test/{keyword}")
# def read_keyword(keyword:str):
#     return {"keyword":keyword}

#http://127.0.0.1:8000/test/checkSystemPythonVersion/os
@app.get('/test/checkSystemPythonVersion/os')
def read_version():
    #version = os.system('python --version')
    stream = os.popen('python --version')
    output = stream.read()
    print(output)
    return output

#http://127.0.0.1:8000/test/checkSystemPythonVersion/subprocess
@app.get('/test/checkSystemPythonVersion/subprocess')
def read_version():
    result = subprocess.run(['python','--version'],
    stdout = subprocess.PIPE, text = True)
    print(result.stdout)
    return result.stdout

#http://127.0.0.1:8000/test/dbtest
@app.get("/test/dbtest")
def process():
    dt_now = datetime.datetime.now()
    print(dt_now)

    conn = MongoClient(dbaddrs,dbport)
    #print(conn)
    #print(conn.list_database_names())

    #db = conn.local
    #col = db.startup_log

    database = conn.shopping
    collection = database.shopping
    scol = database.prodDateSummary

    #cursur
    #seldata = col.find()

    #convert list Type
    dataList = list(collection.find())

    #for문을 사용하여 추가

    for data in dataList:

        searchKey = data['productObj']['prd_id']
        # print('====================================================')
        # print(searchKey)

        #GET
        res = requests.get(naverUrl + searchKey, headers = headers )

        # print(str(res.status_code) + " | " + res.text)
        # print(type(res.text))

        resJson = json.loads(res.text)
        #print(type(resJson))

        # print(resJson['lastBuildDate'])
        # print(resJson['total'])
        # print(resJson['start'])
        # print(resJson['display'])
        # print(resJson['items'])

        searchResultList = resJson['items']

        for sr in searchResultList:

            print(sr['mallName'] + ' // ' + sr['brand'] + ' :: ' + sr['lprice'])

            serchRes = {
                "date":dt_now,
                "name":searchKey,
                "title":sr['title'],
                "link":sr['link'],
                "image":sr['image'],
                "lprice":sr['lprice'],
                "hprice":sr['hprice'],
                "mallName":sr['mallName'],
                "productId":sr['productId'],
                "productType":sr['productType'],
                "brand":sr['brand'],
                "maker":sr['maker'],
                "category1":sr['category1'],
                "category2":sr['category2'],
                "category3":sr['category3'],
                "category4":sr['category4'],
            }

            collection.insert_one(serchRes) #mongodb에 검색 결과 삽입
        print()
    #return {"result":"success"}
    return resJson