import json


# 构造 API 请求数据
def build_api_data(action, params):
    data = {
        'action': action,
        'params': params
    }
    return json.dumps(data)


# 发送 API 请求
async def send_api_request(ws, action, params, suffix=''):
    data = build_api_data(action + suffix, params)
    await ws.send_str(data)
    response = await ws.receive()
    return json.loads(response.data)
