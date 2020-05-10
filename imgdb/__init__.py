import nonebot
from nonebot import on_command, CommandSession
from .data_source import get_random_pic
from .data_source import get_lib_status
from .data_source import get_pic_by_id
__plugin_name__ = '图片'
__plugin_usage__ = r"""从图库随机返图
也可使用 '图片 n'来获得n张图片
查看编号为k的图片，可以输入 '查看图片 k' 
提示：使用以上指令获取的图片是缩略图哦
如要获取高清版，请访问https://example.com/post/图片id
如要查看图库状态，可直接输入 '图库状态'"""

@on_command('getpic', aliases=['图片'],only_to_me=False)
async def getpic(session: CommandSession):
    arg = session.current_arg_text.strip().lower()
    num = 1
    if not arg == '':
        num = int(arg)
    if num > 0:
        if num <=5:
            await session.send('提示：以下是缩略图，如需高清大图，请访问https://example.com\n如果您想为图片添加标签，请输入“帮助 标签”')
            for i in range(0,num):
                content=await get_random_pic()
                if not content == "error":
                    cont = '[CQ:image,file=https://example.com/'+content['thumbnailUrl']+']\n'+'图片id: '+str(content['id'])
                else:
                    cont = '发生了未知错误，请再试一次＞﹏＜'
                await session.send(cont)
                if content['tags'] == []:
                    await session.send('这张图还没有标签呢＞﹏＜')
                else:
                    tag_cont = '图片'+str(content['id'])+'的标签:\n'
                    for tag in content['tags']:
                        for subname in tag['names']:
                            tag_cont += str(subname)+','
                            break
                    await session.send(tag_cont)
        else:
            await session.send('不要一下子吸这么多毒嘛(* ￣︿￣)')
    else:
        await session.send('无效的参数呢')
        
@on_command('lib_stat', aliases=['图库状态'],only_to_me=False)
async def lib_stat(session: CommandSession):
    content=await get_lib_status()
    storage = float(content['diskUsage']/(1024*1024*1024))
    stat = '图库\n图片计数: '+str(content['postCount'])+'\n总计大小: '+str(round(storage,3))+' GB\nhttps://example.com'
    await session.send(stat)

@on_command('img_view', aliases=['view','查看图片'],only_to_me=False)
async def img_view(session: CommandSession):
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send('请输入图片id并重试＞﹏＜')
        return
    content=await get_pic_by_id(arg)
    cont = '[CQ:image,file=https://example.com/'+content['thumbnailUrl']+']\n'+'图片id: '+str(content['id'])
    await session.send(cont)
    if content['tags'] == []:
        await session.send('这张图还没有标签呢＞﹏＜')
    else:
        tag_cont = '标签:'
        for tag in content['tags']:
            for subname in tag['names']:
                tag_cont += '\n' + str(subname)
        await session.send(tag_cont)