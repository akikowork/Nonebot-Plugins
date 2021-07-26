from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import get_latest_dynamic
import json

__plugin_name__ = 'B站动态'
__plugin_usage__ = r"""在莉艾尔推送动态后抓取动态内容
也可手动输入'妖精仓库动态 n'来获取时间倒序为n的动态
不输入n或输入错误时会自动返回最新动态"""

@on_command('bili_dynamic', aliases=('b站动态','本群订阅的','本群订阅的[末日时的妖精仓库](523546844)更新了新的动态。','本群订阅的&#91;末日时的妖精仓库&#93;(523546844)更新了新的动态。','妖精仓库动态'),only_to_me=False)
async def bili_dynamic(session: CommandSession):
    numid = 0
    arg = session.current_arg_text.strip().lower()
    if not arg == '':
        if len(arg) >= 2:
            numid = 0
        else:
            numid = int(arg) - 1
    try:
        cont=json.loads(await get_latest_dynamic())
        conts=cont['data']['cards'][numid]['card']
        j=json.loads(conts)
   # title=j['item']['title']
    #id=j['item']['id']
        description=j['item']['description']
        summary=''
    #if not title == '':
      #  summary ='\n标题: '+title
       # await session.send(summary)
    #summary = '动态id: '+str(id)+summary
        summary = '概要: '+description
        while len(summary) > 174:
            summary=summary[:-1]
        summary +='...'
        await session.send(summary)
        for i in j['item']['pictures']:
            img_src = i['img_src']
            await session.send('[CQ:image,file='+img_src+']')
    except BaseException:
        await session.send('不支持的动态格式＞﹏＜')
    return

@on_natural_language(keywords={'本群订阅的','末日时的妖精仓库','更新了新的动态'},only_to_me=False)
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(80.0, 'bili_dynamic')