import nonebot
from nonebot import on_command, CommandSession
import os, re
import random
from .readJSON import 读JSON文件

__plugin_name__ = '文字生成'
__plugin_usage__ = r"""狗*不通文章生成
用法: 文字生成 主题"""

data = 读JSON文件("C:\\Users\\fze\\Desktop\\Programs\\Messager-bot\\Messager\\plugins\\bullshit_gen\\data.json")
名人名言 = data["famous"] # a 代表前面垫话，b代表后面垫话
前面垫话 = data["before"] # 在名人名言前面弄点废话
后面垫话 = data['after']  # 在名人名言后面弄点废话
废话 = data['bosh'] # 代表文章主要废话来源

xx = "学生会退会"

重复度 = 2

def 洗牌遍历(列表):
    global 重复度
    池 = list(列表) * 重复度
    while True:
        random.shuffle(池)
        for 元素 in 池:
            yield 元素

下一句废话 = 洗牌遍历(废话)
下一句名人名言 = 洗牌遍历(名人名言)

def 来点名人名言():
    global 下一句名人名言
    xx = next(下一句名人名言)
    xx = xx.replace(  "a",random.choice(前面垫话) )
    xx = xx.replace(  "b",random.choice(后面垫话) )
    return xx

def 另起一段():
    xx = ". "
    xx += "\r\n"
    xx += "    "
    return xx

@on_command('bullshit_gen', aliases=['文章生成','文字生成'],only_to_me=False)
async def bullshit_gen(session: CommandSession):
    arg = session.current_arg_text.strip().lower()
    if not arg:
        xx = '中午吃什么'
    else:
        xx = arg
    tmp = str()
    while ( len(tmp) < 170 ) :
        分支 = random.randint(0,100)
        if 分支 < 2:
            tmp += 另起一段()
        elif 分支 < 20 :
            tmp += 来点名人名言()
        else:
            tmp += next(下一句废话)
    tmp = tmp.replace("x",xx)
    await session.send(tmp)