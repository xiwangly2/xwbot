import json

# 导入自己写的模块
from internal.config import config


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


# 发送私聊消息
async def send_private_msg(ws, user_id, message, auto_escape=False):
    params = {
        'user_id': user_id,
        'message': message,
        'auto_escape': auto_escape
    }
    return await send_api_request(ws, 'send_private_msg', params)


# 发送群消息
async def send_group_msg(ws, group_id, message, auto_escape=False):
    params = {
        'group_id': group_id,
        'message': message,
        'auto_escape': auto_escape
    }
    return await send_api_request(ws, 'send_group_msg', params)


# 发送消息
async def send_msg(ws, message_type, user_id=None, group_id=None, message='', auto_escape=False):
    params = {
        'message_type': message_type,
        'message': message,
        'auto_escape': auto_escape
    }
    if message_type == 'private':
        params['user_id'] = user_id
    elif message_type == 'group':
        params['group_id'] = group_id
    return await send_api_request(ws, 'send_msg', params)


# 撤回消息
async def delete_msg(ws, message_id):
    params = {
        'message_id': message_id
    }
    return await send_api_request(ws, 'delete_msg', params)


# 获取消息
async def get_msg(ws, message_id):
    params = {
        'message_id': message_id
    }
    return await send_api_request(ws, 'get_msg', params)


# 获取合并转发消息
async def get_forward_msg(ws, id):
    params = {
        'id': id
    }
    return await send_api_request(ws, 'get_forward_msg', params)


# 发送好友赞
async def send_like(ws, user_id, times=1):
    params = {
        'user_id': user_id,
        'times': times
    }
    return await send_api_request(ws, 'send_like', params)


# 群组踢人
async def set_group_kick(ws, group_id, user_id, reject_add_request=False):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'reject_add_request': reject_add_request
    }
    return await send_api_request(ws, 'set_group_kick', params)


# 群组单人禁言
async def set_group_ban(ws, group_id, user_id, duration=30 * 60):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'duration': duration
    }
    return await send_api_request(ws, 'set_group_ban', params)


# 群组匿名用户禁言
async def set_group_anonymous_ban(ws, group_id, anonymous=None, anonymous_flag=None, duration=30 * 60):
    params = {
        'group_id': group_id,
        'duration': duration
    }
    if anonymous:
        params['anonymous'] = anonymous
    if anonymous_flag:
        params['anonymous_flag'] = anonymous_flag
    return await send_api_request(ws, 'set_group_anonymous_ban', params)


# 群组全员禁言
async def set_group_whole_ban(ws, group_id, enable=True):
    params = {
        'group_id': group_id,
        'enable': enable
    }
    return await send_api_request(ws, 'set_group_whole_ban', params)


# 群组设置管理员
async def set_group_admin(ws, group_id, user_id, enable=True):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'enable': enable
    }
    return await send_api_request(ws, 'set_group_admin', params)


# 群组匿名
async def set_group_anonymous(ws, group_id, enable=True):
    params = {
        'group_id': group_id,
        'enable': enable
    }
    return await send_api_request(ws, 'set_group_anonymous', params)


# 设置群名片（群备注）
async def set_group_card(ws, group_id, user_id, card=''):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'card': card
    }
    return await send_api_request(ws, 'set_group_card', params)


# 设置群名
async def set_group_name(ws, group_id, group_name):
    params = {
        'group_id': group_id,
        'group_name': group_name
    }
    return await send_api_request(ws, 'set_group_name', params)


# 退出群组
async def set_group_leave(ws, group_id, is_dismiss=False):
    params = {
        'group_id': group_id,
        'is_dismiss': is_dismiss
    }
    return await send_api_request(ws, 'set_group_leave', params)


# 设置群组专属头衔
async def set_group_special_title(ws, group_id, user_id, special_title='', duration=-1):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'special_title': special_title,
        'duration': duration
    }
    return await send_api_request(ws, 'set_group_special_title', params)


# 处理加好友请求
async def set_friend_add_request(ws, flag, approve=True, remark=''):
    params = {
        'flag': flag,
        'approve': approve,
        'remark': remark
    }
    return await send_api_request(ws, 'set_friend_add_request', params)


# 处理加群请求／邀请
async def set_group_add_request(ws, flag, sub_type, approve=True, reason=''):
    params = {
        'flag': flag,
        'sub_type': sub_type,
        'approve': approve,
        'reason': reason
    }
    return await send_api_request(ws, 'set_group_add_request', params)


# 获取登录号信息
async def get_login_info(ws):
    return await send_api_request(ws, 'get_login_info', {})


# 获取陌生人信息
async def get_stranger_info(ws, user_id, no_cache=False):
    params = {
        'user_id': user_id,
        'no_cache': no_cache
    }
    return await send_api_request(ws, 'get_stranger_info', params)


# 获取好友列表
async def get_friend_list(ws):
    return await send_api_request(ws, 'get_friend_list', {})


# 获取群信息
async def get_group_info(ws, group_id, no_cache=False):
    params = {
        'group_id': group_id,
        'no_cache': no_cache
    }
    return await send_api_request(ws, 'get_group_info', params)


# 获取群列表
async def get_group_list(ws):
    return await send_api_request(ws, 'get_group_list', {})


# 获取群成员信息
async def get_group_member_info(ws, group_id, user_id, no_cache=False):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'no_cache': no_cache
    }
    return await send_api_request(ws, 'get_group_member_info', params)


# 获取群成员列表
async def get_group_member_list(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'get_group_member_list', params)


# 获取群荣誉信息
async def get_group_honor_info(ws, group_id, honor_type):
    params = {
        'group_id': group_id,
        'type': honor_type
    }
    return await send_api_request(ws, 'get_group_honor_info', params)


# 获取 Cookies
async def get_cookies(ws, domain=''):
    params = {
        'domain': domain
    }
    return await send_api_request(ws, 'get_cookies', params)


# 获取 CSRF Token
async def get_csrf_token(ws):
    return await send_api_request(ws, 'get_csrf_token', {})


# 获取 QQ 相关接口凭证
async def get_credentials(ws, domain=''):
    params = {
        'domain': domain
    }
    return await send_api_request(ws, 'get_credentials', params)


# 获取语音
async def get_record(ws, file, out_format):
    params = {
        'file': file,
        'out_format': out_format
    }
    return await send_api_request(ws, 'get_record', params)


# 获取图片
async def get_image(ws, file):
    params = {
        'file': file
    }
    return await send_api_request(ws, 'get_image', params)


# 检查是否可以发送图片
async def can_send_image(ws):
    return await send_api_request(ws, 'can_send_image', {})


# 检查是否可以发送语音
async def can_send_record(ws):
    return await send_api_request(ws, 'can_send_record', {})


# 获取运行状态
async def get_status(ws):
    return await send_api_request(ws, 'get_status', {})


# 获取版本信息
async def get_version_info(ws):
    return await send_api_request(ws, 'get_version_info', {})


# 重启 OneBot 实现
async def set_restart(ws, delay=0):
    params = {
        'delay': delay
    }
    return await send_api_request(ws, 'set_restart', params)


# 清理缓存
async def clean_cache(ws):
    return await send_api_request(ws, 'clean_cache', {})
