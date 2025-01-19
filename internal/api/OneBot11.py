# 导入自己写的模块
from internal.api.functions import send_api_request


# 发送私聊消息
async def send_private_msg(ws, user_id, message, auto_escape=False, async_call=False, rate_limited=False):
    params = {
        'user_id': user_id,
        'message': message,
        'auto_escape': auto_escape
    }
    suffix = ''
    if async_call:
        suffix = '_async'
    elif rate_limited:
        suffix = '_rate_limited'
    return await send_api_request(ws, 'send_private_msg', params, suffix)


# 发送群消息
async def send_group_msg(ws, group_id, message, auto_escape=False, async_call=False, rate_limited=False):
    params = {
        'group_id': group_id,
        'message': message,
        'auto_escape': auto_escape
    }
    suffix = ''
    if async_call:
        suffix = '_async'
    elif rate_limited:
        suffix = '_rate_limited'
    return await send_api_request(ws, 'send_group_msg', params, suffix)


# 发送消息
async def send_msg(ws, message_type, user_id=None, group_id=None, message='', auto_escape=False, async_call=False,
                   rate_limited=False):
    params = {
        'message_type': message_type,
        'message': message,
        'auto_escape': auto_escape
    }
    if message_type == 'private':
        params['user_id'] = user_id
    elif message_type == 'group':
        params['group_id'] = group_id
    suffix = ''
    if async_call:
        suffix = '_async'
    elif rate_limited:
        suffix = '_rate_limited'
    return await send_api_request(ws, 'send_msg', params, suffix)


# 撤回消息
async def delete_msg(ws, message_id, async_call=False):
    params = {
        'message_id': message_id
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'delete_msg', params, suffix)


# 获取消息
async def get_msg(ws, message_id):
    params = {
        'message_id': message_id
    }
    return await send_api_request(ws, 'get_msg', params)


# 获取合并转发消息
async def get_forward_msg(ws, _id):
    params = {
        'id': _id
    }
    return await send_api_request(ws, 'get_forward_msg', params)


# 发送好友赞
async def send_like(ws, user_id, times=1, async_call=False):
    params = {
        'user_id': user_id,
        'times': times
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'send_like', params, suffix)


# 群组踢人
async def set_group_kick(ws, group_id, user_id, reject_add_request=False, async_call=False):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'reject_add_request': reject_add_request
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_kick', params, suffix)


# 群组单人禁言
async def set_group_ban(ws, group_id, user_id, duration=30 * 60, async_call=False):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'duration': duration
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_ban', params, suffix)


# 群组匿名用户禁言
async def set_group_anonymous_ban(ws, group_id, anonymous=None, anonymous_flag=None, duration=30 * 60,
                                  async_call=False):
    params = {
        'group_id': group_id,
        'duration': duration
    }
    if anonymous:
        params['anonymous'] = anonymous
    if anonymous_flag:
        params['anonymous_flag'] = anonymous_flag
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_anonymous_ban', params, suffix)


# 群组全员禁言
async def set_group_whole_ban(ws, group_id, enable=True, async_call=False):
    params = {
        'group_id': group_id,
        'enable': enable
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_whole_ban', params, suffix)


# 群组设置管理员
async def set_group_admin(ws, group_id, user_id, enable=True, async_call=False):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'enable': enable
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_admin', params, suffix)


# 群组匿名
async def set_group_anonymous(ws, group_id, enable=True, async_call=False):
    params = {
        'group_id': group_id,
        'enable': enable
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_anonymous', params, suffix)


# 设置群名片（群备注）
async def set_group_card(ws, group_id, user_id, card='', async_call=False):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'card': card
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_card', params, suffix)


# 设置群名
async def set_group_name(ws, group_id, group_name, async_call=False):
    params = {
        'group_id': group_id,
        'group_name': group_name
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_name', params, suffix)


# 退出群组
async def set_group_leave(ws, group_id, is_dismiss=False, async_call=False):
    params = {
        'group_id': group_id,
        'is_dismiss': is_dismiss
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_leave', params, suffix)


# 设置群组专属头衔
async def set_group_special_title(ws, group_id, user_id, special_title='', duration=-1, async_call=False):
    params = {
        'group_id': group_id,
        'user_id': user_id,
        'special_title': special_title,
        'duration': duration
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_special_title', params, suffix)


# 处理加好友请求
async def set_friend_add_request(ws, flag, approve=True, remark='', async_call=False):
    params = {
        'flag': flag,
        'approve': approve,
        'remark': remark
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_friend_add_request', params, suffix)


# 处理加群请求／邀请
async def set_group_add_request(ws, flag, sub_type, approve=True, reason='', async_call=False):
    params = {
        'flag': flag,
        'sub_type': sub_type,
        'approve': approve,
        'reason': reason
    }
    suffix = '_async' if async_call else ''
    return await send_api_request(ws, 'set_group_add_request', params, suffix)


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


# 隐藏 API
# 对事件执行快速操作#
async def handle_quick_operation(ws, context, operation):
    params = {
        'context': context,
        'operation': operation
    }
    return await send_api_request(ws, '.handle_quick_operation', params)
