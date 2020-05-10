import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import re
import json
async def get_news() -> str:
    session = requests.Session()
    url = f"http://ic.snssdk.com/2/article/v25/stream/"
    result = json.loads(requests.get(url).content)
    return result