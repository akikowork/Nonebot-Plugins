import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import re
import json


async def get_latest_dynamic() -> str:
    session = requests.Session()
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=523546844&offset_dynamic_id=0&need_top=0"
    print(requests.get(url).content)
    return requests.get(url).content