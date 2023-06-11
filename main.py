import asyncio
import json
import os
import time

import aiohttp
import yaml

# 导入自己写的模块
from chat_thesaurus import *
from mysql import Database

# 机器人配置信息
if os.path.exists('config/config.yml'):
    with open('config/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
else:
    with open('config/config_example.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)


# 构造 API 请求数据
def build_api_data(action, params):
    data = {
        'action': action,
        'params': params
    }
    return json.dumps(data)


# 发送 API 请求
async def send_api_request(session, ws, action, params):
    data = build_api_data(action, params)
    await ws.send_str(data)
    response = await ws.receive()
    return json.loads(response.data)


# 接收消息
async def receive_messages(ws):
    event = {"action": "get_login_info", "params": {"access_token": config['access_token']}}
    await ws.send_str(json.dumps(event))


# 发送消息
async def send_message(session, ws, messages, text, auto_escape=False):
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
    await send_api_request(session, ws, 'send_msg', params)


async def while_msg(session, ws):
    try:
        # 控制跳出
        try:
            # 接收返回的消息
            response = await ws.receive()
        except Exception:
            print("[", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "] Connection is lost")
            await asyncio.sleep(60)
            raise StopIteration
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
            Database(config).chat_logs(messages)

        # 查找词库获取回答
        text = await chat_thesaurus(messages, config)
        if text is None:
            raise StopIteration    
        await send_message(session, ws, messages, text, False)
        text = None
    except Exception:
        pass


# 运行机器人
async def run_bot():
    async with aiohttp.ClientSession() as session:
        try:
            ws = await session.ws_connect(f"ws://{config['host']}:{config['port']}/",
                                          headers={"Authorization": f"Bearer {config['access_token']}"})
        except:
            print("Error creating websocket connection")
            return
        
        await receive_messages(ws)
        while True:
            await while_msg(session, ws)


if __name__ == '__main__':
    asyncio.run(run_bot())
