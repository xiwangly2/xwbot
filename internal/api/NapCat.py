# 导入自己写的模块
from internal.functions import send_api_request


# 群签到
async def set_group_sign(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'set_group_sign', params)


# 群聊戳一戳
async def group_poke(ws, group_id, user_id):
    params = {
        'group_id': group_id,
        'user_id': user_id
    }
    return await send_api_request(ws, 'group_poke', params)


# 私聊戳一戳
async def friend_poke(ws, user_id):
    params = {
        'user_id': user_id
    }
    return await send_api_request(ws, 'friend_poke', params)


# 获取推荐好友/群聊卡片
async def ArkSharePeer(ws, user_id=None, phoneNumber=None, group_id=None):
    params = {}
    if user_id:
        params['user_id'] = user_id
    if phoneNumber:
        params['phoneNumber'] = phoneNumber
    if group_id:
        params['group_id'] = group_id
    return await send_api_request(ws, 'ArkSharePeer', params)


# 获取推荐群聊卡片
async def ArkShareGroup(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'ArkShareGroup', params)


# 获取机器人账号范围
async def get_robot_uin_range(ws):
    return await send_api_request(ws, 'get_robot_uin_range', {})


# 设置在线状态
async def set_online_status(ws, status, ext_status, battery_status):
    params = {
        'status': status,
        'ext_status': ext_status,
        'battery_status': battery_status
    }
    return await send_api_request(ws, 'set_online_status', params)


# 获取分类的好友列表
async def get_friends_with_category(ws):
    return await send_api_request(ws, 'get_friends_with_category', {})


# 设置QQ头像
async def set_qq_avatar(ws, file):
    params = {
        'file': file
    }
    return await send_api_request(ws, 'set_qq_avatar', params)


# 获取文件信息
async def get_file(ws, file_id):
    params = {
        'file_id': file_id
    }
    return await send_api_request(ws, 'get_file', params)


# 转发到私聊
async def forward_friend_single_msg(ws, message_id, user_id):
    params = {
        'message_id': message_id,
        'user_id': user_id
    }
    return await send_api_request(ws, 'forward_friend_single_msg', params)


# 转发到群聊
async def forward_group_single_msg(ws, message_id, group_id):
    params = {
        'message_id': message_id,
        'group_id': group_id
    }
    return await send_api_request(ws, 'forward_group_single_msg', params)


# 英译中
async def translate_en2zh(ws, words):
    params = {
        'words': words
    }
    return await send_api_request(ws, 'translate_en2zh', params)


# 设置表情回复
async def set_msg_emoji_like(ws, message_id, emoji_id):
    params = {
        'message_id': message_id,
        'emoji_id': emoji_id
    }
    return await send_api_request(ws, 'set_msg_emoji_like', params)


# 发送合并转发
async def send_forward_msg(ws, message_type, user_id=None, group_id=None, messages=None):
    params = {
        'message_type': message_type,
        'user_id': user_id,
        'group_id': group_id,
        'messages': messages
    }
    return await send_api_request(ws, 'send_forward_msg', params)


# 设置私聊已读
async def mark_private_msg_as_read(ws, user_id):
    params = {
        'user_id': user_id
    }
    return await send_api_request(ws, 'mark_private_msg_as_read', params)


# 设置群聊已读
async def mark_group_msg_as_read(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'mark_group_msg_as_read', params)


# 获取私聊历史记录
async def get_friend_msg_history(ws, user_id, message_seq='0', count=20, reverseOrder=False):
    params = {
        'user_id': user_id,
        'message_seq': message_seq,
        'count': count,
        'reverseOrder': reverseOrder
    }
    return await send_api_request(ws, 'get_friend_msg_history', params)


# 创建收藏
async def create_collection(ws):
    return await send_api_request(ws, 'create_collection', {})


# 获取收藏
async def get_collection_list(ws):
    return await send_api_request(ws, 'get_collection_list', {})


# 设置签名
async def set_self_longnick(ws, longNick):
    params = {
        'longNick': longNick
    }
    return await send_api_request(ws, 'set_self_longnick', params)


# 获取私聊历史记录
async def get_recent_contact(ws, count=10):
    params = {
        'count': count
    }
    return await send_api_request(ws, 'get_recent_contact', params)


# 标记所有已读
async def mark_all_as_read(ws):
    return await send_api_request(ws, 'mark_all_as_read', {})


# 获取自身点赞列表
async def get_profile_like(ws):
    return await send_api_request(ws, 'get_profile_like', {})


# 获取自定义表情
async def fetch_custom_face(ws, count=48):
    params = {
        'count': count
    }
    return await send_api_request(ws, 'fetch_custom_face', params)


# AI文字转语音
async def get_ai_record(ws, character, group_id, text):
    params = {
        'character': character,
        'group_id': group_id,
        'text': text
    }
    return await send_api_request(ws, 'get_ai_record', params)


# 获取AI语音角色列表
async def get_ai_characters(ws, group_id, chat_type):
    params = {
        'group_id': group_id,
        'chat_type': chat_type
    }
    return await send_api_request(ws, 'get_ai_characters', params)


# 群聊发送AI语音
async def send_group_ai_record(ws, character, group_id, text):
    params = {
        'character': character,
        'group_id': group_id,
        'text': text
    }
    return await send_api_request(ws, 'send_group_ai_record', params)


# 群聊/私聊戳一戳
async def send_poke(ws, user_id, group_id=None):
    params = {
        'user_id': user_id
    }
    if group_id:
        params['group_id'] = group_id
    return await send_api_request(ws, 'send_poke', params)
