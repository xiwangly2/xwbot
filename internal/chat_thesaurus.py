import base64
import html
import json
import platform
import re

import aiohttp
import requests

from internal.api.MessageBuilder import MessageBuilder
from internal.api.OneBot11 import send_msg, get_forward_msg, send_like, delete_msg, set_group_special_title, \
    get_group_member_info
from internal.api.gocqhttp import check_url_safely
from internal.config import config
from internal.database.db_handler import get_bot_switch, set_bot_switch, set_chat_logs
from internal.format_output import clear_terminal, print_error


def parse_message(messages):
    try:
        if messages['message']:
            message = html.unescape(messages['message'])
            arg = re.split(r'\s', message)
            arg_len = len(arg)
        else:
            message = ''
            arg = ['']
            arg_len = 0

        if arg_len > 1:
            match = re.search(re.escape(arg[0]) + r' (.*)', message)
            arg_all = match.group(1) if match else None
        else:
            arg_all = None
    except Exception:
        if config['debug']:
            import traceback
            traceback.print_exc()
        else:
            pass
        message = ''
        arg = ['']
        arg_len = 0
        arg_all = None

    return message, arg, arg_len, arg_all


# 判断QQ号是否在管理员列表里
def f_is_admin(user_id):
    return f"{user_id}" in config['admin']


# 判断 url 是否安全
async def is_safe_url(ws, url):
    result = await check_url_safely(ws, url)
    # 响应数据
    # 字段	类型	说明
    # level	int	安全等级, 1: 安全 2: 未知 3: 危险
    if config['debug']:
        print(f"URL: {url} 安全等级: {result['data']['level']}")
    if result['data']['level'] == 1:
        return True
    else:
        return False


async def handle_loli_command():
    try:
        api_url = 'https://www.dmoe.cc/random.php?return=json'
        response = requests.get(api_url)
        img_url = response.json()['imgurl']
        return {'text_list': ['您要的loli:', MessageBuilder.image(img_url)]}
    except Exception:
        if config['debug']:
            import traceback
            traceback.print_exc()
        return "获取loli失败: 网络错误"


async def handle_math_command(arg, arg_len):
    if arg_len == 1:
        return "/math method x y y"
    data = {}
    if arg_len >= 5:
        data['z'] = arg[4]
    if arg_len >= 4:
        data['y'] = arg[3]
    if arg_len >= 3:
        data['x'] = arg[2]
    if arg_len >= 2:
        data['m'] = arg[1]
    async with aiohttp.ClientSession():
        response = requests.post(url="https://api.xiwangly.com/math.php", data=data)
        return f"{response.text}"


# noinspection PyPackageRequirements,PyProtectedMember
async def screenshot_command(arg, arg_len):
    import platform

    # 获取系统架构
    arch = platform.machine()
    # 判断是否为 x86_64 或 aarch64
    if arch in ['x86_64', 'aarch64', 'AMD64', 'arm64']:
        if arg_len == 1:
            return "/screenshot url [full_page=False] or /prtsc url [full_page=False]"
        elif arg_len > 3:
            return "参数过多"

        full_page = arg_len == 3

        from playwright.async_api import async_playwright
        from playwright._impl._errors import Error

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            try:
                await page.goto(arg[1])
                screenshot_bytes = await page.screenshot(full_page=full_page)
                base64_image = base64.b64encode(screenshot_bytes).decode()
                base64_image = f"base64://{base64_image}"
                return ['已截图:', MessageBuilder.image(base64_image)]
            except Error as e:
                return f"无法访问链接: {arg[1]} 错误: {str(e)}"
            finally:
                await browser.close()
    else:
        return f"当前功能不支持系统架构: {arch}"


async def chat_thesaurus(messages, ws=None, chat_ai_process=None):
    message, arg, arg_len, arg_all = parse_message(messages)
    is_admin = f_is_admin(messages['user_id'])

    try:
        # 查询开关
        bot_switch = get_bot_switch(messages['group_id'])
        if bot_switch is None or bot_switch.switch == '0':
            if arg[0] == '/on' and is_admin:
                set_bot_switch(messages['group_id'], '1')
                return "Bot started successfully."
            else:
                return None
    except NameError:
        bot_switch = None
        if config['debug']:
            import traceback
            traceback.print_exc()
        pass

    if bot_switch.switch == '1':
        if arg[0] == '/on' and is_admin:
            return "Bot is running."
        elif arg[0] == '/off' and is_admin:
            set_bot_switch(messages['group_id'], '0')
            return "Bot is off."
        elif arg[0] == '/CQ' and is_admin:
            set_bot_switch(messages['group_id'], 'CQ')
            return "Bot transitioned to CQ state."
        elif arg[0] == '/AI' and is_admin:
            set_bot_switch(messages['group_id'], 'AI')
            return "Bot transitioned to AI state."
        elif arg[0] == '/help':
            return "这是一个帮助列表<Response [200]>"
        elif arg[0] == '/来份萝莉' or arg[0] == '/loli':
            return await handle_loli_command()
        elif arg[0] == '/math':
            if arg_len == 1:
                return "/math method x y z"
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
                return await handle_math_command(arg, arg_len)
        elif arg[0] == '/calc':
            import math
            try:
                return eval(arg_all, {"__builtins__": None}, {"math": math})
            except ArithmeticError:
                return "计算错误，表达式不合法"
        elif arg[0] == '/uuid':
            import uuid
            if arg_len == 1:
                return str(uuid.uuid4())
            elif arg_len == 3:
                return str(uuid.uuid5(arg[1], arg[2]))
            else:
                return "参数错误"
        elif arg[0] == '/screenshot' or arg[0] == '/prtsc':
            if is_admin:
                return await screenshot_command(arg, arg_len)
            elif arg_len == 2:
                if await is_safe_url(ws, arg[1]):
                    return await screenshot_command(arg, arg_len)
                else:
                    return '链接不安全'
            else:
                return '参数错误'
        elif arg[0] == '/send' and is_admin:
            return ['已发送:', re.sub(r'/send ', '', message)]
        elif arg[0] == '/like':
            await send_like(ws, messages['user_id'], 20)
            return {
                'text_list': ['已赞']
            }
        elif re.search(r'^\[CQ:reply,id=(\d+)].*?/del$', message) and is_admin:
            match = re.search(r'\[CQ:reply,id=(\d+)]', message)
            if match:
                message_id = match.group(1)
                await delete_msg(ws, message_id)
                return "已撤回"
            else:
                return "未找到消息ID"
        elif arg[0] == '/test':
            # 测试
            # return ['第一条消息', '第二条消息']
            return {
                'auto_escape': False,
                'text_list': ['第一条消息', '第二条消息',
                              {
                                  "type": "face",
                                  "data": {
                                      "id": "123"
                                  }
                              }]
            }
        elif arg[0] == '/菜单':
            return """
            /on 开启机器人
            /off 关闭机器人
            ……
            """
        elif arg[0] == '/shell' and is_admin:
            # Dangerous command
            # 你应该知道你要做什么
            import subprocess
            try:
                # check os
                if platform.system() == 'Windows':
                    result = subprocess.check_output(arg_all, shell=True, encoding='gbk')
                else:
                    result = subprocess.check_output(arg_all, shell=True).decode()

                # Split result into chunks of 2048 characters
                chunk_size = 2048
                result_chunks = [result[i:i + chunk_size] for i in range(0, len(result), chunk_size)]
                return result_chunks
            except subprocess.CalledProcessError as e:
                return str(e)
        elif arg[0] == '/set_group_special_title':
            role = await get_group_member_info(ws, messages['group_id'], messages['self_id'])
            role = role['data']['role']
            if role == 'owner':
                if arg_len == 3 and re.search(r'\[CQ:at,qq=(\d+)]', arg[1]) and is_admin:
                    # /set_group_special_title @user title
                    await set_group_special_title(ws, messages['group_id'], re.sub(r'\[CQ:at,qq=(\d+)]', r'\1', arg[1]),
                                                  arg[2])
                    text = "为用户[CQ:at,qq=" + re.sub(r'\[CQ:at,qq=(\d+)]', r'\1', arg[1]) + "]设置了群组专属头衔：" + \
                           arg[2]
                elif arg_len == 3 and re.match(r'^\d+$', arg[1]) and is_admin:
                    # /set_group_special_title user_id title
                    await set_group_special_title(ws, messages['group_id'], arg[1], arg[2])
                    text = "为用户[CQ:at,qq=" + arg[1] + "]设置了群组专属头衔：" + arg[2]
                elif arg_len == 3:
                    text = '不是管理员只能为自己设置群组专属头衔'
                elif arg_len == 2 and is_admin:
                    # /set_group_special_title title
                    await set_group_special_title(ws, messages['group_id'], messages['user_id'], arg[1])
                    text = "为管理员自己设置了群组专属头衔：" + arg[1]
                elif arg_len == 2:
                    # /set_group_special_title title
                    # TODO: 为自己设置群组专属头衔 可能需要敏感词过滤
                    await set_group_special_title(ws, messages['group_id'], messages['user_id'], arg[1])
                    text = "为自己设置了群组专属头衔：" + arg[1]
                else:
                    text = '/set_group_special_title [user_id]* title'
            else:
                text = '不是群主无法设置群组专属头衔'
            return text
        else:
            return None
    elif bot_switch.switch == 'CQ':
        if arg[0] == '/on' and is_admin:
            set_bot_switch(messages['group_id'], '1')
            return "Bot transitioned to Running state."
        elif arg[0] == '/off' and is_admin:
            set_bot_switch(messages['group_id'], '0')
            return "Bot is off."
        elif re.search(r'\[CQ:xml,data=', message):
            text = html.unescape(message)
            text = re.sub(r'\[CQ:xml,data=(.+)]', r'\1', text)
            return {
                'auto_escape': True,
                'text_list': ['解析XML:', text]
            }
        elif re.search(r'\[CQ:json,data=(.+)]', message):
            text = html.unescape(message)
            text = re.sub(r'\[CQ:json,data=(.+)]', r'\1', text)
            return {
                'auto_escape': True,
                'text_list': ['解析JSON:', text]
            }
        elif re.search(r'\[CQ:forward,id=', message):
            message_id = re.sub(r'\[CQ:forward,id=(.+)]', r'\1', message)
            text = await get_forward_msg(ws, message_id)
            return {
                'auto_escape': True,
                'text_list': ['解析合并转发:', text]
            }
        elif re.search(r'(.+)?/(.+)?pic(.+)?', message):
            from internal.pic import pic
            # 表情包功能
            return await pic(messages, ws)
        elif re.search(r'^\[CQ:at,qq=', message) or re.search(r'^\[CQ:reply,id=', message) or re.search(
                r'^\[CQ:face,id=', message):
            # 不处理at、回复、表情开头的CQ码防止刷屏
            return None
        elif re.search(r'^<\?xml', message, re.DOTALL) and is_admin:
            return ['发送XML:', MessageBuilder.xml(message)]
        elif re.search(r'^\{', message, re.DOTALL) and is_admin:
            return ['发送JSON:', MessageBuilder.json(message)]
        elif re.search(r'\[CQ:.+]', message):
            return {
                'auto_escape': True,
                'text_list': ['解析CQ码:', message]
            }
        else:
            return None
    elif bot_switch.switch == 'AI':
        if arg[0] == '/on' and is_admin:
            set_bot_switch(messages['group_id'], '1')
            return "Bot transitioned to Running state."
        elif arg[0] == '/off' and is_admin:
            set_bot_switch(messages['group_id'], '0')
            return "Bot is off."
        else:

            # 将消息发送到 chat_ai 进程
            chat_ai_process.input_queue.put((messages, messages['message']))

            # 获取 chat_ai 进程的回复
            if not chat_ai_process.output_queue.empty():
                result = chat_ai_process.output_queue.get()
                if result == 'no reply' or result is None:
                    return None
                else:
                    return result.rstrip('\n')
    else:
        return None


async def while_msg(ws, chat_ai_process=None):
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
                set_chat_logs(messages)

            # 查找词库获取回答
            text = await chat_thesaurus(messages, ws, chat_ai_process)
            if text is None:
                continue
            if isinstance(text, str):
                await send_msg(ws, messages['message_type'], user_id=messages.get('user_id'),
                               group_id=messages.get('group_id'), message=text, auto_escape=False, async_call=True)
            elif 'text_list' in text:
                # auto_escape 消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效
                text.setdefault('auto_escape', None)
                for message in text['text_list']:
                    await send_msg(ws, messages['message_type'], user_id=messages.get('user_id'),
                                   group_id=messages.get('group_id'), message=message, auto_escape=text['auto_escape'],
                                   async_call=True)
            else:
                for message in text:
                    await send_msg(ws, messages['message_type'], user_id=messages.get('user_id'),
                                   group_id=messages.get('group_id'), message=message, auto_escape=False,
                                   async_call=True)
        except Exception:
            if config['debug']:
                import traceback
                traceback.print_exc()
            else:
                pass
