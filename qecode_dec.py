import nonebot
import pyzbar.pyzbar as pyzbar
from PIL import Image
import requests
from io import BytesIO
import json
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
__plugin_name__ = '二维码解码'
__plugin_usage__ = r"""解码二维码
用法：
解码 图片
返回图片所包含内容"""

@on_command('qrcode_dec', aliases=['二维码解码', '解码二维码', 'deqrc', '解码'],only_to_me=False)
async def qrcode_dec(session: CommandSession):
    img_src = session.get('img_src', prompt='请提供图片')
    img_url = img_src[56:-1]
    response = requests.get(img_url)
    source = pyzbar.decode(Image.open(BytesIO(response.content)), symbols=[pyzbar.ZBarSymbol.QRCODE])
    if source == []:
        await session.send('未识别到二维码')
        return
    tmp = source[0][0]
    print(tmp)
    tmp = tmp.decode('utf8')
    await session.send('解码结果:\n'+tmp)
    return
@qrcode_dec.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['img_src'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请重新提供')

    session.state[session.current_key] = stripped_arg