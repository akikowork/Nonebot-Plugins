import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
__plugin_name__ = '二维码生成'
__plugin_usage__ = r"""生成二维码
用法：
qrcode 内容
返回包含内容的二维码"""

@on_command('qrcode_gen', aliases=['二维码生成', '生成二维码', 'qrcode', 'qr_code'],only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send('请输入生成二维码的内容并重试')
        return
    arg = arg.replace(' ','_')
    source = '[CQ:image,file=http://qr.topscan.com/api.php?text='+arg+']'
    await session.send(source)
    return
