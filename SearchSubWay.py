import requests
from bs4 import BeautifulSoup
import json
import re
import os
import pandas as pd
import jsonpath
import math

url = 'http://map.amap.com/service/subway?_1469083453978&srhdata=3100_drw_shanghai.json'
url_info='http://map.amap.com/service/subway?_1469083453980&srhdata=3100_info_shanghai.json'

def get_subwayinfo_from(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    html_dict = json.loads(html)
    content_json = jsonpath.jsonpath(html_dict, expr='$..st[*]')
    content_json_new = json.dumps(content_json, ensure_ascii=False)  # dict 变 json
    str=pd.read_json(content_json_new,orient='records')
    return html

# def get_station_info(subwayinfo):
#     station_info={}
#     for line in subwayinfo:
#         station=subwayinfo['n']
#      return station_info

subwayinfo=get_subwayinfo_from(url)

def build_connection(subwayinfo):
    cities_connection = defaultdict(list)
    cities = list(subwayinfo.keys())
    for c1 in cities:
        for c2 in cities:
            if c1 == c2: continue
            if get_city_distance(c1, c2) < threshold:
                cities_connection[c1].append(c2)
    return cities_connection


#print(subwayinfo)


import json
import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


def get_message(ID, cityname, name):
    """
    地铁线路信息获取
    """
    url = 'http://map.amap.com/service/subway?_1469083453978&srhdata=' + ID + '_drw_' + cityname + '.json'
    #url = 'http://map.amap.com/service/subway?_1469083453978&srhdata=3100_drw_shanghai.json'
    #url_info = 'http://map.amap.com/service/subway?_1469083453980&srhdata=3100_info_shanghai.json'
    response = requests.get(url=url, headers=headers)
    html = response.text
    result = json.loads(html)
    for i in result['l']:
        for j in i['st']:
            # 判断是否含有地铁分线
            if len(i['la']) > 0:
                with open('subway.csv', 'a+', encoding='gbk') as f:
                    f.write(name + ',' + i['ln'] + '(' + i['la'] + ')' + ',' + j['n']+ ',' + j['sl'] + '\n')
            else:
                print(name, i['ln'], j['n']+ ',' + j['sl'])
                with open('subway.csv', 'a+', encoding='gbk') as f:
                    f.write(name + ',' + i['ln'] + ',' + j['n'] + ',' + j['sl']+ '\n')


def get_city_info(city_coordination):
    city_location = {}
    for line in city_coordination.split("\n"):
        if line.strip() == "": continue
        city = re.findall("n:'(\w+)'", line)[0]
        x_y = re.findall("Coord:\[(\d+.\d+),\s(\d+.\d+)\]", line)[0]
        x_y = tuple(map(float, x_y))
        city_location[city] = x_y
    return city_location


# def get_city(ID):
#     """
#     城市信息获取
#     """
#     url = 'http://map.amap.com/subway/index.html?&'+ID
#     response = requests.get(url=url, headers=headers)
#     html = response.text
#     # 编码
#     html = html.encode('ISO-8859-1')
#     html = html.decode('utf-8')
#     soup = BeautifulSoup(html, 'lxml')
#     # 城市列表
#     res1 = soup.find_all(class_="city-list fl")[0]
#     res2 = soup.find_all(class_="more-city-list")[0]
#     for i in res1.find_all('a'):
#         # 城市ID值
#         ID = i['id']
#         # 城市拼音名
#         cityname = i['cityname']
#         # 城市名
#         name = i.get_text()
#         get_message(ID, cityname, name)
#     for i in res2.find_all('a'):
#         # 城市ID值
#         ID = i['id']
#         # 城市拼音名
#         cityname = i['cityname']
#         # 城市名
#         name = i.get_text()
#         get_message(ID, cityname, name)

subway_info=get_message('3100','shanghai','上海')

print(subway_info)



# def build_connection(subway_info):
#     stations_connection = defaultdict(list)
#     stations = list(subway_info.keys())
#     for c1 in stations:
#         for c2 in stations:
#             if c1 == c2: continue
#             if get_city_distance(c1, c2) < threshold:
#                 cities_connection[c1].append(c2)
#     return cities_connection
