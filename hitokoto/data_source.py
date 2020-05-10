import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import re
import json


async def get_hitokoto(cate: str) -> str:
    if cate == '':
        cate = 'a'
    if cate < 'a':
        cate = 'a'
    if cate > 'g':
        cate = 'a'
    session = requests.Session()
    url = "https://api.imjad.cn/hitokoto/?cat="+cate+"&encode=json"
    result = json.loads(requests.get(url).content)
    return result