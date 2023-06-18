import json
from colorama import Fore, Style

# 导入自己写的模块
from config import config
from chat_thesaurus import chat_thesaurus
from mysql import Database

# 输出红色错误消息的函数
def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)


# 输出黄色警告消息的函数
def print_warning(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)

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
    await send_api_request(ws, 'send_msg', params)


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
                print_error("Error: [", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "] Connection is lost")
                await ws.close()
                break
            # 定义可能不存在的键，防止报错
            messages = json.loads(response.data)
            messages.setdefault('post_type', None)
            messages.setdefault('message_type', None)
            messages.setdefault('group_id', '0')
            messages.setdefault('user_id', '0')

            if messages['post_type'] != "message":
                raise StopIteration

            if config['debug']:
                print(messages)

            if config['write_log']:
                # 日志写入数据库
                Database().chat_logs(messages)

            # 查找词库获取回答
            text = await chat_thesaurus(messages)
            if text is None:
                raise StopIteration    
            if isinstance(text, str):
                await send_message(ws, messages, text, False)
            else:
                if 'text_list' in text:
                    text.setdefault('auto_escape', False)
                    for message in text['text_list']:
                        await send_message(ws, messages, message, text['auto_escape'])
                else:
                    for message in text:
                        await send_message(ws, messages, message, False)
            text = None
        except Exception:
            pass

# 清空终端窗口输出的函数
def clear_terminal():
    import os
    # 尝试使用 os.system('cls') 清空终端窗口输出（Windows）
    try:
        os.system('cls')
        return
    except:
        pass

    # 尝试使用 os.system('clear') 清空终端窗口输出（类Unix）
    try:
        os.system('clear')
        return
    except:
        pass

    # 尝试使用 ANSI 转义序列清空终端窗口输出
    try:
        print("\033c", end='')
        return
    except:
        pass