from googletrans import Translator
import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
__plugin_name__ = '翻译'
__plugin_usage__ = r"""谷歌翻译
调用谷歌api进行文本翻译"""

@on_command('translate', aliases=['翻译'],only_to_me=False)
async def translate(session: CommandSession):
    source = session.get('source', prompt='请输入要翻译的文本')
    if len(source) >= 5000:
        await session.send('超过5000字符上限')
        return
    translator = Translator(service_urls=['translate.google.cn'])
    text = translator.translate(source,dest='zh-cn').text
    detected = translator.detect(source)
    await session.send('检查到语言: '+str(detected.lang)+' 可能性: '+str(detected.confidence*100)+'%')
    while len(text) >= 176:
        await session.send(text[:175])
        text = text[175:]
    if len(text) > 0:
        await session.send(text)
@translate.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    print(stripped_arg)
    if session.is_first_run:
        if stripped_arg:
            session.state['source'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请重新提供文本')

    session.state[session.current_key] = stripped_arg