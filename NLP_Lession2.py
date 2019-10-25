import requests
from bs4 import BeautifulSoup
import json
import re
import os
import pandas as pd

import jsonpath

url = 'http://map.amap.com/service/subway?_1469083453978&srhdata=3100_drw_shanghai.json'

url_info='http://map.amap.com/service/subway?_1469083453980&srhdata=3100_info_shanghai.json'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

#json字符串转换为python字典对象
html_dict = json.loads(html)
content_json=jsonpath.jsonpath(html_dict,expr='$..st[*]')
#print(content_json)
str=content_json[0]
#print(str)


content_json_new = json.dumps(content_json,ensure_ascii=False) # dict 变 json
print(content_json_new)

# print(str) #['xiaohei'] 返回的是一个列表
# print(html)
# t = jsonpath.jsonpath(dic,'$..s')   #当不存在hehe这个key时，返回false
# print(t)  #False

str=pd.read_json(content_json_new,orient='records')
print(str)