from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.ft.v20200304 import ft_client, models 
import requests
import re
import os
import urllib
from bs4 import BeautifulSoup
import nonebot
import json
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

__plugin_name__ = '人脸动漫风'
__plugin_usage__ = r"""人脸动漫风
请@我 转动漫 '图片'"""

@on_command('animationate', aliases=['转动漫'],only_to_me=True)
async def animationate(session: CommandSession):
    img_src = session.get('img_src', prompt='请提供图片')
    img_url = img_src[img_src.find('url=')+4:]
    try: 
        cred = credential.Credential("your token", "your token") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ft.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ft_client.FtClient(cred, "ap-shanghai", clientProfile) 

        req = models.FaceCartoonPicRequest()
        params = '{\"Url\":\"'+img_url+'\",\"RspImgType\":\"url\"}'
        req.from_json_string(params)

        resp = client.FaceCartoonPic(req)
        print(resp.to_json_string())
        ans = json.loads(resp.to_json_string())
        await session.send('[CQ:image,file='+ans['ResultUrl']+']')

    except TencentCloudSDKException as err: 
        await session.send('没有检测到人脸或发生了错误＞﹏＜') 
        return

@animationate.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    
    print(stripped_arg)
    if session.is_first_run:
        if stripped_arg:
            session.state['img_src'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请重新提供')
    session.state[session.current_key] = stripped_arg
