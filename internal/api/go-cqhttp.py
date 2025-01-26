from internal.api.functions import send_api_request


# TODO: 还没写完
# 设置登录号资料
async def set_qq_profile(ws, profile):
    params = {
        'profile': profile
    }
    return await send_api_request(ws, 'set_qq_profile', params)


# 获取在线机型
async def get_model_show(ws):
    return await send_api_request(ws, '_get_model_show', {})


# 设置在线机型
async def set_model_show(ws, model):
    params = {
        'model': model
    }
    return await send_api_request(ws, '_set_model_show', params)


# 获取当前账号在线客户端列表
async def get_online_clients(ws):
    return await send_api_request(ws, 'get_online_clients', {})


# 删除好友
async def delete_friend(ws, user_id):
    params = {
        'user_id': user_id
    }
    return await send_api_request(ws, 'delete_friend', params)


# 标记消息已读
async def mark_msg_as_read(ws, message_id):
    params = {
        'message_id': message_id
    }
    return await send_api_request(ws, 'mark_msg_as_read', params)


# 发送合并转发 (群聊)
async def send_group_forward_msg(ws, group_id, messages):
    params = {
        'group_id': group_id,
        'messages': messages
    }
    return await send_api_request(ws, 'send_group_forward_msg', params)


# 发送合并转发 (好友)
async def send_private_forward_msg(ws, user_id, messages):
    params = {
        'user_id': user_id,
        'messages': messages
    }
    return await send_api_request(ws, 'send_private_forward_msg', params)


# 获取群消息历史记录
async def get_group_msg_history(ws, group_id, message_seq):
    params = {
        'group_id': group_id,
        'message_seq': message_seq
    }
    return await send_api_request(ws, 'get_group_msg_history', params)


# 图片 OCR
async def ocr_image(ws, image):
    params = {
        'image': image
    }
    return await send_api_request(ws, 'ocr_image', params)


# 获取群系统消息
async def get_group_system_msg(ws):
    return await send_api_request(ws, 'get_group_system_msg', {})


# 获取精华消息列表
async def get_essence_msg_list(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'get_essence_msg_list', params)


# 获取群 @全体成员 剩余次数
async def get_group_at_all_remain(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'get_group_at_all_remain', params)


# 设置群头像
async def set_group_portrait(ws, group_id, file):
    params = {
        'group_id': group_id,
        'file': file
    }
    return await send_api_request(ws, 'set_group_portrait', params)


# 设置精华消息
async def set_essence_msg(ws, message_id):
    params = {
        'message_id': message_id
    }
    return await send_api_request(ws, 'set_essence_msg', params)


# 移出精华消息
async def delete_essence_msg(ws, message_id):
    params = {
        'message_id': message_id
    }
    return await send_api_request(ws, 'delete_essence_msg', params)


# 群打卡
async def send_group_sign(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'send_group_sign', params)


# 发送群公告
async def send_group_notice(ws, group_id, content):
    params = {
        'group_id': group_id,
        'content': content
    }
    return await send_api_request(ws, '_send_group_notice', params)


# 获取群公告
async def get_group_notice(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, '_get_group_notice', params)


# 上传群文件
async def upload_group_file(ws, group_id, file):
    params = {
        'group_id': group_id,
        'file': file
    }
    return await send_api_request(ws, 'upload_group_file', params)


# 删除群文件
async def delete_group_file(ws, group_id, file_id):
    params = {
        'group_id': group_id,
        'file_id': file_id
    }
    return await send_api_request(ws, 'delete_group_file', params)


# 创建群文件文件夹
async def create_group_file_folder(ws, group_id, folder_name):
    params = {
        'group_id': group_id,
        'folder_name': folder_name
    }
    return await send_api_request(ws, 'create_group_file_folder', params)


# 删除群文件文件夹
async def delete_group_folder(ws, group_id, folder_id):
    params = {
        'group_id': group_id,
        'folder_id': folder_id
    }
    return await send_api_request(ws, 'delete_group_folder', params)


# 获取群文件系统信息
async def get_group_file_system_info(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'get_group_file_system_info', params)


# 获取群根目录文件列表
async def get_group_root_files(ws, group_id):
    params = {
        'group_id': group_id
    }
    return await send_api_request(ws, 'get_group_root_files', params)


# 获取群子目录文件列表
async def get_group_files_by_folder(ws, group_id, folder_id):
    params = {
        'group_id': group_id,
        'folder_id': folder_id
    }
    return await send_api_request(ws, 'get_group_files_by_folder', params)


# 获取群文件资源链接
async def get_group_file_url(ws, group_id, file_id):
    params = {
        'group_id': group_id,
        'file_id': file_id
    }
    return await send_api_request(ws, 'get_group_file_url', params)


# 上传私聊文件
async def upload_private_file(ws, user_id, file):
    params = {
        'user_id': user_id,
        'file': file
    }
    return await send_api_request(ws, 'upload_private_file', params)


# 下载文件到缓存目录
async def download_file(ws, url):
    params = {
        'url': url
    }
    return await send_api_request(ws, 'download_file', params)


# 检查链接安全性
async def check_url_safely(ws, url):
    params = {
        'url': url
    }
    return await send_api_request(ws, 'check_url_safely', params)


# 对事件执行快速操作 (隐藏 API)
async def handle_quick_operation(ws, context, operation):
    params = {
        'context': context,
        'operation': operation
    }
    return await send_api_request(ws, '.handle_quick_operation', params)
