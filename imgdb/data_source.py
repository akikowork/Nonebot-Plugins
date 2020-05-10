import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import re
import json
import random
session = requests.Session()
headers = {
        'Accept':'application/json',
        'Content-Type':'application/json',
        }
async def get_lib_status() -> str:
    url='https://example.com/api/info'
    content = session.get(url, headers=headers)
    return json.loads(content.content)

async def get_random_pic() -> str:
    stat = await get_lib_status()
    counts = stat['postCount']
    url='https://example.com/api/post/'+str(random.randint(0,counts))
    response = session.get(url, headers=headers)
    if str(response) == '<Response [200]>':
        return json.loads(response.content)
    else:
        url='https://example.com/api/post/'+str(random.randint(0,counts))
        response = session.get(url, headers=headers)
        if str(response) == '<Response [200]>':
            return json.loads(response.content)
        else:
            url='https://example.com/api/post/'+str(random.randint(0,counts))
            response = session.get(url, headers=headers)
            if str(response) == '<Response [200]>':
                return json.loads(response.content)
            else:
                return "error"
async def get_pic_by_id(post_id: str) -> str:
    url='https://example.com/api/post/'+post_id
    response = session.get(url, headers=headers)
    if str(response) == '<Response [200]>':
        return json.loads(response.content)
    else:
        await session.send('发生了错误＞﹏＜，此id不存在或图库离线')
        return