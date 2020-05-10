import nonebot
from nonebot import on_command, CommandSession
import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import re
import json
__plugin_name__ = '标签'
__plugin_usage__ = r"""向szurubooru图库中的图片添加标签
用法：
添加标签 图片id 标签1 标签2 标签3...
多个标签请以空格分隔"""

@on_command('add_tag', aliases=['添加标签','tagging'],only_to_me=False)
async def add_tag(session: CommandSession):
    arg = session.current_arg_text.strip().lower().split()
    if len(arg) < 2:
        await session.send('输入有误，用法： \n添加标签 图片id 标签1 标签2 标签3...')
        return
    post_id = str(arg[0])
    arg.pop(0)
    tags_list = arg
    reque = requests.Session()
    await session.send('正在处理图片'+post_id)
    url = "https://example.com/api/post/" + post_id
    headers = {
            'Accept':'application/json',
            'Authorization':'',
            'Cookie':'',
            'Content-Type':'application/json',
            }
            
    response = reque.get(url, headers=headers)
    img_info = json.loads(response.content)
    versions = img_info['version']
    tags_orig = []
    for tag in img_info['tags']:
        tags_orig.append(tag['names'][0])
    for tag in tags_list:
        if not tag in tags_orig:
            tags_orig.append(tag)
    payloads = {
            'version':'4',
            'tags':[''],
            }
    payloads['version'] =str(versions)
    payloads['tags'] = tags_orig
    response = reque.put(url,data=json.dumps(payloads), headers=headers)
    if not str(response) == '<Response [200]>':
        await session.send('发生错误，请求未被受理＞﹏＜')
    else:
        tags_new = ''
        for i in tags_orig:
            tags_new+=str(i)+' '
        await session.send('图片: '+post_id+' 现在的标签为: '+tags_new)
        
@on_command('del_tag', aliases=['删除标签','detag'])
async def del_tag(session: CommandSession):
    arg = session.current_arg_text.strip().lower().split()
    if len(arg) < 2:
        await session.send('输入有误，用法： \n删除标签 图片id 标签1 标签2 标签3...')
        return
    post_id = str(arg[0])
    arg.pop(0)
    tags_list = arg
    reque = requests.Session()
    await session.send('正在处理图片'+post_id)
    url = "https://example.com/api/post/" + post_id
    headers = {
            'Accept':'application/json',
            'Authorization':'',
            'Cookie':'',
            'Content-Type':'application/json',
            }
            
    response = reque.get(url, headers=headers)
    img_info = json.loads(response.content)
    versions = img_info['version']
    tags_orig = []
    for tag in img_info['tags']:
        tags_orig.append(tag['names'][0])
    for i in tags_list:
        if i in tags_orig:
            tags_orig.remove(i)
    payloads = {
            'version':'4',
            'tags':[''],
            }
    payloads['version'] =str(versions)
    payloads['tags'] = tags_orig
    response = reque.put(url,data=json.dumps(payloads), headers=headers)
    if not str(response) == '<Response [200]>':
        await session.send('发生错误，请求未被受理＞﹏＜')
    else:
        tags_new = ''
        for i in tags_orig:
            tags_new+=str(i)+' '
        await session.send('图片: '+post_id+' 现在的标签为: '+tags_new)