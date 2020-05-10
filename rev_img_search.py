import requests
import re
import os
import urllib
from bs4 import BeautifulSoup
import nonebot
from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

__plugin_name__ = '反向搜图'
__plugin_usage__ = r"""反向搜图
请@我 搜图 '图片'"""

async def send_req(url):
    api_source = 'https://iqdb.org'
    session_req = requests.Session()
    resp = session_req.post(api_source,data={"url":str(url)})
    return resp.content

@on_command('rev_img_search', aliases=['搜图', '找图', '查图'],only_to_me=True)
async def rev_img_search(session: CommandSession):
    img_src = session.get('img_src', prompt='请提供图片')
    await session.send('注意: 本功能耗时较长，请耐心等待')
    img_url = img_src[56:-1]
    try:
        res = await send_req(img_url)
        soup = BeautifulSoup(res,'html.parser')
        p_nodes = soup.find_all('img')
        p_sources = soup.find_all('a')
        IMAGE_TEMP = 'C:/Users/fze/Desktop/Programs/CQPro/data/image/tmp_prev.jpg'
        url_ = 'https://www.iqdb.org'+p_nodes[1].get('src')
        urllib.request.urlretrieve(url_,IMAGE_TEMP)
        await session.send('最佳匹配:\n[CQ:image,file=tmp_prev.jpg]\n'+'https:'+p_sources[1].get('href'))
        print(p_nodes[1].get('src'))
        print(url_)
    except BaseException:
        await session.send('远端服务器响应时间过长，请重试＞﹏＜')
    return

@rev_img_search.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    
    print(stripped_arg)
    if session.is_first_run:
        if stripped_arg:
            session.state['img_src'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请重新提供图片')

    session.state[session.current_key] = stripped_arg