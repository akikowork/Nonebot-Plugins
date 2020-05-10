from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import requests
__plugin_name__ = '随机图片'
__plugin_usage__ = r"""随机图片
随机返回二次元图片
用法：Cs图"""
@on_command('setu', aliases=('车来', '随机图片', '二次元', 'Cs图', '老婆', 'setu'),only_to_me=False)
async def random_pic_global(session: CommandSession):
    req = requests.Session()
    url = 'http://api.mtyqx.cn/api/random.php'
    img_src = requests.get(url).url
    await session.send(f'[CQ:image,file={img_src}]')
