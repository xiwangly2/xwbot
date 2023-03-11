import asyncio
import os
import traceback
import yaml
import time
import websocket
import json
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
def send_api_request(ws, action, params):
    data = build_api_data(action, params)
    ws.send(data)
    response = ws.recv()
    return json.loads(response)

# 接收消息
def receive_messages(ws):
    event = {"action": "get_login_info", "params": {"access_token": config['access_token']}}
    ws.send(json.dumps(event))

# 发送消息
def send_message(message, message_type, target_id, auto_escape = False):
    params = {
        'message': message,
        'auto_escape': auto_escape
    }
    if(message_type == 'group'):
        params['group_id'] = target_id
    elif(message_type == 'private'):
        params['user_id'] = target_id
    send_api_request(ws, 'send_msg', params)

async def while_msg(ws):
    try:
        # 控制跳出
        try:
            # 接收返回的消息
            response = ws.recv()
        except Exception:
            print("[", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "] Connection is lost")
            time.sleep(60)
            raise StopIteration
        # 定义可能不存在的键，防止报错
        messages = json.loads(response)
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
        text = chat_thesaurus(messages, config)
        if text == None:
            raise StopIteration
        
        if messages['message_type'] == 'private':
            # 处理私聊消息
            # TODO: 根据收到的消息内容进行相应处理
            send_message(text, 'private', messages['user_id'])
        elif messages['message_type'] == 'group':
            # 处理群聊消息
            # TODO: 根据收到的消息内容进行相应处理
            send_message(text, 'group', messages['group_id'])
    except Exception:
        pass

# 运行机器人
def run_bot(ws):
    receive_messages(ws)
    while True:
        asyncio.run(while_msg(ws))

if __name__ == '__main__':
    # 尝试建立websocket连接
    try:
        ws = websocket.create_connection(f"ws://{config['host']}:{config['port']}/", header=[f"Authorization: Bearer {config['access_token']}"])
    except:
        print("Error creating websocket connection")
        traceback.print_exc()
        exit()
    run_bot(ws)
