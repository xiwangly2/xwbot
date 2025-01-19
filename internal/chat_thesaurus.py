import html
import json
import re

import aiohttp
import requests

from internal.database.database import Database
from internal.format_output import clear_terminal, print_error
# 导入自己写的模块
from internal.api.OneBot11 import send_msg, get_forward_msg, send_like, delete_msg
from internal.config import config
from internal.pic import pic


# 判断QQ号是否在管理员列表里
def f_is_admin(target_id):
    if f"{target_id}" in config['admin']:
        return True
    else:
        return False


async def chat_thesaurus(messages, ws=None):
    # 消息文本内容
    if messages['message']:
        message = html.unescape(messages['message'])
        # 按空格分隔参数
        arg = re.split(r'\s', message)
        # 计算参数数量
        arg_len = len(arg)
    else:
        message = ''
        arg = ['']
        arg_len = 0
    # 捕获一个命令后的所有内容
    if arg_len > 1:
        match = re.match(arg[0] + ' (.*)', message)
        if match:
            arg_all = match.group(1)
        else:
            arg_all = None
    else:
        arg_len = 1
        arg_all = None

    is_admin = f_is_admin(messages['user_id'])
    try:
        # 查询开关
        bot_switch = Database().db_handler.bot_switch(messages['group_id'])
        if bot_switch is None:
            if arg[0] == '/on' and is_admin:
                Database().db_handler.bot_switch(messages['group_id'], 1)
            text = "Bot started successfully."
            return text
    except NameError:
        bot_switch = False
        if config['debug']:
            import traceback
            traceback.print_exc()
        pass
    if bot_switch is False:
        if arg[0] == '/on' and is_admin:
            Database().db_handler.bot_switch(messages['group_id'], 1)
            text = "Bot started successfully."
        else:
            text = None
        return text
    elif bot_switch is True:
        if arg[0] == '/on' and is_admin:
            text = "Bot is running."
        elif arg[0] == '/off' and is_admin:
            Database().db_handler.bot_switch(messages['group_id'], 0)
            text = "Bot is off."
        elif arg[0] == '/help':
            text = "这是一个帮助列表<Response [200]>"
        elif arg[0] == '/来份萝莉' or arg[0] == '/loli':
            # 发送随机二次元图片
            api_url = 'https://api.xiwangly.top/random.php?return=json'
            response = requests.get(api_url)
            img_url = response.json()['imgurl']
            text = {
                'text_list': ['您要的loli:', f"[CQ:image,file={img_url}]"]
            }
        elif arg[0] == '/math':
            if arg_len == 1:
                text = "/math method x y z"
            else:
                data = {}
                if arg_len >= 5:
                    try:
                        data['z'] = arg[4]
                    except NameError:
                        pass
                if arg_len >= 4:
                    try:
                        data['y'] = arg[3]
                    except NameError:
                        pass
                if arg_len >= 3:
                    try:
                        data['x'] = arg[2]
                    except NameError:
                        pass
                if arg_len >= 2:
                    try:
                        data['m'] = arg[1]
                    except NameError:
                        pass
                async with aiohttp.ClientSession():
                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
                    }
                    response = requests.post(url="https://api.xiwangly.com/math.php", data=data, headers=header)
                    text = f"{response}"
        elif re.match(r'_http(s)://', message):
            text = "这是一个???"
        elif re.match(r'\d{1,3}', message):
            text = "选项"
        elif arg[0] == '/calc':
            import math
            try:
                text = eval(arg_all, {"__builtins__": None}, {"math": math})
            except ArithmeticError:
                text = "计算错误，表达式不合法"
        elif arg[0] == '/uuid':
            import uuid
            if arg_len == 1:
                text = str(uuid.uuid4())
            elif arg_len == 3:
                text = str(uuid.uuid5(arg[1], arg[2]))
            else:
                text = "参数错误"
        elif arg[0] == '/send' and is_admin:
            text = {
                'text_list': ['已发送:', arg[1]]
            }
        elif arg[0] == '/like':
            await send_like(ws, messages['user_id'], 3)
            text = {
                'text_list': ['已赞']
            }
        elif re.search(r'^\[CQ:reply,id=(\d+)\].*?/del$', message) and is_admin:
            match = re.search(r'\[CQ:reply,id=(\d+)\]', message)
            if match:
                message_id = match.group(1)
                await delete_msg(ws, message_id)
                text = {
                    'text_list': ['已撤回']
                }
            else:
                text = "未找到消息ID"
        elif config['debug']:
            if arg[0] == '/test':
                # 测试
                # text = ['第一条消息', '第二条消息']
                text = {
                    'auto_escape': True,
                    'text_list': ['第一条消息', '第二条消息', f"原始消息:{message}"]
                }
            else:
                text = None
        elif arg[0] == '/菜单':
            text = '********************\n\
/菜单 或 /help -帮助\n\
[1]/ping ip\n\
/复读 [format] msg(admin)\n\
/start - 开始\n\
[2]/来份萝莉 或 /loli - 发送随机二次元图片\n\
[3]/uuid - 生成UUID\n\
/dwz url - 生成短网址\n\
/m msg - 智能聊天（实验）\n\
/yiyan - 随机一言\n\
/info - 信息\n\
/dic question answer - 增加dic(admin)\n\
/math [x] [y] [z] method - 数学计算\n\
/xuid id - 查询xbox xuid\n\
/fileupload url [name] - 文件上传(admin)\n\
/签到 或 /check_in - 每日签到\n\
/gold user(object) number - 增加金币(admin)\n\
注：[]表示参数可选，部分命令可通过[]的数字简化选择\n\
********************'
        elif re.match(r'\[CQ\:xml,data\=', message):
            text = html.unescape(message)
            text = re.sub(r'\[CQ:xml,data=(.+)\]', r'\1', text)
            text = {
                'auto_escape': True,
                'text_list': ['解析XML:', text]
            }
        elif re.match(r'\[CQ:json,data=(.+)\]', message):
            text = html.unescape(message)
            text = re.sub(r'\[CQ:json,data=(.+)\]', r'\1', text)
            text = {
                'auto_escape': True,
                'text_list': ['解析JSON:', text]
            }
        elif re.match(r'\[CQ\:forward,id\=', message):
            message_id = re.sub(r'\[CQ:forward,id=(.+)\]', r'\1', message)
            text = await get_forward_msg(ws, message_id)
            text = {
                'auto_escape': True,
                'text_list': ['解析合并转发:', text]
            }
        elif re.match(r'^\[CQ\:at,qq=', message) or re.match(r'^\[CQ\:reply,id=', message) or re.match(
                r'^\[CQ\:face,id=', message):
            # 不处理at、回复、表情开头的CQ码防止刷屏
            text = None
        elif re.match(r'\[CQ\:image.+\]', message):
            text = {
                'auto_escape': True,
                'text_list': ['解析图像:', message]
            }
        elif re.match(r'(.+)?\/(.+)?pic(.+)?', message):
            # 表情包功能
            text = await pic(messages, ws)
        elif re.match(r'\[CQ\:.+\]', message):
            text = {
                'auto_escape': True,
                'text_list': ['解析CQ码:', message]
            }
        elif re.match(r'^\<\?xml', message, re.DOTALL) and is_admin:
            text = message
            json_data = {
                'type': 'xml',
                'data': {'data': text}
            }
            text = {
                'auto_escape': True,
                'text_list': ['发送XML:', json_data]
            }
        elif re.match(r'^\{', message, re.DOTALL) and is_admin:
            text = message
            json_data = {
                'type': 'json',
                'data': {'data': text}
            }
            text = ['发送JSON:', json_data]
        else:
            text = None
        return text


async def while_msg(ws):
    while True:
        try:
            # 控制跳出
            try:
                # 接收返回的消息
                response = await ws.receive()
                if ws.closed:
                    raise StopAsyncIteration
            except Exception:
                import time
                # 清空终端窗口输出
                clear_terminal()
                print_error("[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "] Connection is lost.")
                await ws.close()
                break
            # 定义可能不存在的键，防止报错
            messages = json.loads(response.data)
            messages.setdefault('post_type', None)
            messages.setdefault('message_type', None)
            messages.setdefault('meta_event_type', None)
            messages.setdefault('group_id', '0')
            messages.setdefault('user_id', '0')
            messages.setdefault('message', '')

            # 心跳包
            if messages['meta_event_type'] == "heartbeat":
                continue

            if config['debug']:
                print(messages)

            if config['write_log']:
                # 日志写入数据库
                Database().db_handler.chat_logs(messages)

            # 查找词库获取回答
            text = await chat_thesaurus(messages, ws)
            if text is None:
                continue
            if isinstance(text, str):
                await send_msg(ws, messages['message_type'], user_id=messages.get('user_id'),
                               group_id=messages.get('group_id'), message=text, auto_escape=False, async_call=True)
            elif 'text_list' in text:
                # auto_escape 控制自动格式化消息，这里默认否，即消息不处理CQ码等格式
                text.setdefault('auto_escape', False)
                for message in text['text_list']:
                    await send_msg(ws, messages['message_type'], user_id=messages.get('user_id'),
                                   group_id=messages.get('group_id'), message=message, auto_escape=text['auto_escape'], async_call=True)
            else:
                for message in text:
                    await send_msg(ws, messages['message_type'], user_id=messages.get('user_id'),
                                   group_id=messages.get('group_id'), message=message, auto_escape=False, async_call=True)
        except Exception:
            if config['debug']:
                import traceback
                traceback.print_exc()
            else:
                pass
