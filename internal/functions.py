import json
from colorama import Fore, Style

# 导入自己写的模块
from internal.config import config
from internal.chat_thesaurus import chat_thesaurus
from internal.database.database import Database


# 输出红色错误消息的函数
def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)


# 输出黄色警告消息的函数
def print_warning(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)


def print_green(message):
    print(Fore.GREEN + message + Style.RESET_ALL)


# 构造 API 请求数据
def build_api_data(action, params):
    data = {
        'action': action,
        'params': params
    }
    return json.dumps(data)


# 发送 API 请求
async def send_api_request(ws, action, params):
    data = build_api_data(action, params)
    await ws.send_str(data)
    response = await ws.receive()
    return json.loads(response.data)


# 接收消息
async def receive_messages(ws):
    event = {"action": "get_login_info", "params": {"access_token": config['access_token']}}
    await ws.send_str(json.dumps(event))


# 获取群 @全体成员 剩余次数
async def get_group_at_all_remain(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'get_group_at_all_remain', params)


# 获取群系统消息
async def get_group_system_msg(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'get_group_system_msg', params)


# 获取消息
async def get_msg(ws, message_id):
    params = {
        'message_id': message_id
    }
    return await send_api_request(ws, 'get_msg', params)


# 发送消息
async def send_message(ws, messages, text, auto_escape=False):
    params = {
        'message': text,
        'auto_escape': auto_escape
    }
    if messages['message_type'] == 'private':
        # 处理私聊消息
        params['user_id'] = messages['user_id']
    elif messages['message_type'] == 'group':
        # 处理群聊消息
        params['group_id'] = messages['group_id']
    return await send_api_request(ws, 'send_msg', params)


# 解析合并转发
async def get_forward_msg(ws, message_id):
    params = {
        'message_id': message_id
    }
    return await send_api_request(ws, 'get_forward_msg', params)


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
                print_error("Error: [" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "] Connection is lost.")
                await ws.close()
                break
            # 定义可能不存在的键，防止报错
            messages = json.loads(response.data)
            messages.setdefault('post_type', None)
            messages.setdefault('message_type', None)
            messages.setdefault('meta_event_type', None)
            messages.setdefault('group_id', '0')
            messages.setdefault('user_id', '0')

            if messages['meta_event_type'] == "heartbeat":
                raise StopIteration

            if config['debug']:
                print(messages)

            if config['write_log']:
                # 日志写入数据库
                Database().db_handler.chat_logs(messages)

            # 查找词库获取回答
            text = await chat_thesaurus(messages, ws)
            if text is None:
                raise StopIteration
            if isinstance(text, str):
                await send_message(ws, messages, text, False)
            else:
                if 'text_list' in text:
                    # auto_escape 控制自动格式化消息，这里默认否，即消息不处理CQ码等格式
                    text.setdefault('auto_escape', False)
                    for message in text['text_list']:
                        await send_message(ws, messages, message, text['auto_escape'])
                else:
                    for message in text:
                        await send_message(ws, messages, message, False)
        except Exception:
            pass


# 清空终端窗口输出的函数
def clear_terminal():
    import os
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        pass
