import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import re
import json
import random
img_host = "https://example.com/"
session = requests.Session()
headers = {
        'Accept':'application/json',
        'Content-Type':'application/json',
        }
async def get_lib_status() -> str:
    url = img_host + 'api/info'
    content = session.get(url, headers=headers)
    return json.loads(content.content)

async def get_random_pic() -> str:
    stat = await get_lib_status()
    counts = stat['postCount']
    url = img_host + 'api/post/'+str(random.randint(0,counts))
    response = session.get(url, headers=headers)
    if str(response) == '<Response [200]>':
        return json.loads(response.content)
    else:
        url = img_host + 'api/post/'+str(random.randint(0,counts))
        response = session.get(url, headers=headers)
        if str(response) == '<Response [200]>':
            return json.loads(response.content)
        else:
            url = img_host + 'api/post/'+str(random.randint(0,counts))
            response = session.get(url, headers=headers,verify=False)
            if str(response) == '<Response [200]>':
                return json.loads(response.content)
            else:
                return "error"
async def get_pic_by_id(post_id: str) -> str:
    url = img_host + 'api/post/'+post_id
    response = session.get(url, headers=headers)
    if str(response) == '<Response [200]>':
        return json.loads(response.content)
    else:
        return "-1"
