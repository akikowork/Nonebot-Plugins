import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import re
import pypinyin
import json

session = requests.Session()

token = "your weatherbit token"

async def get_weather_of_city(citys: str) -> str:
    session = requests.Session()
    city = ''
    for i in pypinyin.pinyin(citys, style=pypinyin.NORMAL):
        city += ''.join(i)
    url_= f'https://api.weatherbit.io/v2.0/current?key={token}&city={city}&lang=zh'
    r = requests.get(url_).content
    if r == b'':
        return 'error'
    items = json.loads(r)
    items = items['data'][0]
    return items