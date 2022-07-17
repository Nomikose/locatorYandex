import time
import requests
import json
import sqlite3

from requests import Response

conn = sqlite3.connect(r'C:/Users/Dell/PycharmProjects/locatorYandex/cidbase.db')
cur = conn.cursor()
print("Подключен к SQLite3")
cur.execute("""CREATE TABLE IF NOT EXISTS cid_table(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   operator INT NOT NULL,
   cellid INT NOT NULL,
   lac INT NOT NULL,
   latitude REAL NOT NULL,
   longitude REAL NOT NULL,
   precision REAL NOT NULL,
   CONSTRAINT unq UNIQUE (operator, cellid, lac));
""")
conn.commit()

url = "http://api.lbs.yandex.net/geolocation"
headers = {'Content-Type': 'application/json'}

CountryCode = 250
operator = 2
lac = 7830

for cid in range(200064513, 200064515):
    time.sleep(0.001)
    print("CID=" + str(cid))
    data = {
        "common": {
            "version":"1.0",
            "api_key":"ADa39mABAAAAykYiCQIA-qBwJ729XwvNmaV8sodmUWi_LMYAAAAAAAAAAADhjuV4ek-hRixusY1h4KA7ztFo2g=="
        },
        "gsm_cells": [
            {
                "countrycode": CountryCode,
                "operatorid": operator,
                "cellid": cid,
                "lac": lac
            }
        ]
    }
    json.dumps(data)
    response = requests.post(url, data=("json=" + json.dumps(data)), headers=headers)
    # print(response.status_code)
    if response.status_code == 200:
        print("SUCCESS!")
    else:
        print("An error has occurred.")
    print(response.json())
    dictList = json.loads(response.text)
    # print(dictList['position']['precision'])
    latitude = dictList['position']['latitude']
    longitude = dictList['position']['longitude']
    precision = dictList['position']['precision']

    sqlite_insert_with_param = """INSERT INTO cid_table(operator, cellid, lac, latitude, longitude, precision)
                                  VALUES (?, ?, ?, ?, ?, ?);"""
    data_from_api = (operator, cid, lac, latitude, longitude, precision)
    # print(data_from_api)

    if precision != 100000.0:
        cur.execute(sqlite_insert_with_param, data_from_api)
        conn.commit()
    else:
        print("NOT FOUND!")

cur.close()

'''
cur.execute("""INSERT INTO cid_table(operator, cellid, lac, latitude, longitude, precision) 
           VALUES(2, 222, 7835, 59.92725372314453, 30.38752555847168, 385.8784484863281);""")
conn.commit()
'''

'''
cur.execute("Delete FROM cid_table;")
conn.commit()
'''

'''
r = requests.post("http://api.lbs.yandex.net/geolocation", data=("json=" + json.dumps(data)), headers=headers)

print(r.status_code)
print(r.headers)
# print(r.text)
print(r.json())
dictData = r.text

dictList = json.loads(dictData)
# print(dictList)
'''