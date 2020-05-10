import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import get_hitokoto

__plugin_name__ = '一言'
__plugin_usage__ = r"""每日一言
指令名称: '一言','每日一言','鸡汤'
如要指定分类，可在命令后加上参数，留空或有误默认为动画
分类说明
参数值	含义
a	Anime - 动画
b	Comic - 漫画
c	Game - 游戏
d	Novel - 小说
e	原创
f	来自网络
g	其他"""


@on_command('hitokoto', aliases=['一言','每日一言','鸡汤'],only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip().lower()
    if arg == '':
        arg = 'a'
    cont = await get_hitokoto(arg)
    await session.send(cont['hitokoto'])
        