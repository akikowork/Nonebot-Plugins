from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
from .data_source import get_weather_of_city

__plugin_name__ = '详细天气'
__plugin_usage__ = r"""天气查询
详细天气  [城市名称]
注意：查询国际天气要使用英文名。
如：Tokyo、Los Angels"""

@on_command('weather_detail', aliases=('详细天气'),only_to_me=False)
async def weather_detail(session: CommandSession):
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    items = await get_weather_of_city(city)
    if items == 'error':
        await session.send('未查询到有关信息')
        return
    cont = f'{city}的天气报告:'
    cont += '\n纬度: '+str(items['lat'])+'°'
    cont += '\n经度: '+str(items['lon'])+'°'
    tim = (int(items['ob_time'][-5:-3])+8) % 24
    cont += '\n数据观测时间: '+str(items['ob_time'][:-5])+str(tim)+str(items['ob_time'][-3:])+' UTC +8'
    cont += '\n时区: '+items['timezone']
    cont += '\n日/夜: '
    if items['pod'] == 'd':
        cont+='日间'
    else:
        cont+='夜间'
    cont += '\n湿度: '+str(items['rh'])+'%'
    cont += '\n气压: '+str(items['pres']/1000)+'个大气压'
    cont += '\n能见度: '+str(items['vis'])+'千米'
    cont += '\n风速: '+str(items['wind_spd'])+'米/秒'
    cont += '\n云覆盖率: '+str(items['clouds'])+'%'
    await session.send(cont)
    cont = ''
    cont += '预计太阳辐射: '+str(items['solar_rad'])+'瓦特/平方米'
    cont += '\n风向: '+str(items['wind_dir'])+'° '+items['wind_cdir_full']
    tim = (int(items['sunrise'][:2])+8)%24
    cont += '\n日出时间: '+str(tim)+items['sunrise'][2:]
    tim = (int(items['sunset'][:2])+8)%24
    cont += '\n日落时间: '+str(tim)+items['sunset'][2:]
    cont += '\n降雪: '+str(items['snow'])+'毫米/小时'
    cont += '\n太阳仰角: '+str(items['elev_angle'])+'°'
    cont += '\n太阳时角: '+str(items['h_angle'])+'°'
    await session.send(cont)
    cont = ''
    cont += '紫外线指数: '+str(items['uv'])+' （0-11+）'
    cont += '\n空气质量指数: '+str(items['aqi'])+' （美国-EPA标准 0-500）'
    cont += '\n成露点: '+str(items['dewpt'])+'℃'
    cont += '\n温度: '+str(items['temp'])+'℃'
    cont += '\n体感温度: '+str(items['app_temp'])+'℃'
    cont += '\n[CQ:image,file=https://www.weatherbit.io/static/img/icons/'+items['weather']['icon']+'.png]'
    cont += '\n'+items['weather']['description']
    await session.send(cont)

@weather_detail.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg
    