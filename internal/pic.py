import asyncio
import html
import json
import re


async def pic(messages, ws=None):
    # 消息文本内容
    message = html.unescape(messages['message'])
    # 按空格分隔参数
    arg = re.split(r'\s', message)
    # 计算参数数量
    arg_len = len(arg)
    if arg[0] == '/pic':
        text = "/pic 功能使用指南:\n\
/randpic ……\n\
"
    elif arg[0] == '/randpic':
        # TODO: 随机表情包
        if arg_len == 1:
            text = {
                'auto_escape': False,
                'text_list': ['命令为:' + arg[0] + "用于随机返回图片"]
            }
        else:
            if arg_len >= 2:
                try:
                    text = "参数为:"
                    text = {
                        'auto_escape': False,
                        'text_list': ['命令为:' + arg[0], text + arg[1]]
                    }
                except NameError:
                    pass
    elif arg[0] == '/showpic':
        # TODO: 显示表情包
        if arg_len >= 2:
            try:
                text = {
                    'auto_escape': False,
                    'text_list': ['***.jpg', "text + arg[1]"]
                }
            except NameError:
                pass
    elif re.match(r'(.+)?\/savepic(.+)?', message):
        # TODO: 保存表情包
        if arg_len >= 2:
            matches = re.findall(r'\[CQ:reply,id=(-?\d+)\]', message)
            if matches:
                reply_id = matches[0]
                # reply_msg = await get_msg(ws, reply_id)
                
                data = {
                    'action': 'get_msg',
                    'params': {
                        'message_id': reply_id
                    }
                }
                json1 = json.dumps(data)
                await ws.send_str(json1)
                response = await ws.receive()
                reply_msg = json.loads(response.data)
                text = {
                    'auto_escape': False,
                    'text_list': [message, "reply id = " + reply_id, "reply_msg = " + reply_msg]
                }
    elif arg[0] == '/mvpic':
        # TODO: 移动/重命名表情包
        pass
    elif arg[0] == '/cppic':
        # TODO: 复制表情包
        pass
    else:
        text = None
    return text


async def main():
    # 测试
    messages = {...}  # 消息内容

    text = await pic(messages)
    print(text)


if __name__ == '__main__':
    asyncio.run(main())
