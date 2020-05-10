import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import get_news

__plugin_name__ = '新闻'
__plugin_usage__ = r"""每日新闻
指令名称: '新闻','每日新闻'
用法: 新闻 条数
默认抓取3条"""

@on_command('news', aliases=['新闻','每日新闻'],only_to_me=False)
async def _(session: CommandSession):
    cont = await get_news()
    ender = 3
    arg = session.current_arg_text.strip().lower()
    if not arg:
        ender = 3
    elif int(arg) > 5:
        await session.send('信息量太大了＞﹏＜')
        return
    else:
        ender = int(arg)
    if not cont:
        await session.send('发生了未知错误＞﹏＜')
        return
    await session.send('头条新闻:')
    for i in range(0,ender):
        #title = cont['data'][i]['feed_title']
        extract = cont['data'][i]['abstract']
        await session.send(str(i+1)+'.'+extract)
        
    #await session.send(cont['hitokoto'])