import re
import traceback
import asyncio
import aiohttp

from mysql import Database


# 判断QQ号是否在管理员列表里
def f_is_admin(target_id, config):
    if f"{target_id}" in config['admin']:
        return True
    else:
        return False


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def chat_thesaurus(messages, config):
    # 消息文本内容
    message = messages['message']
    # 按空格分隔参数
    arg = re.split('\s', message)
    # 计算参数数量
    arg_len = len(arg)
    # 捕获一个命令后的所有内容
    if arg_len > 1:
        try:
            arg_all = re.match(arg[0] + ' (.*)', message).group(1)
        except NameError:
            pass
    else:
        arg_len = 1

    is_admin = f_is_admin(messages['user_id'], config)
    try:
        # 查询开关
        bot_switch = Database(config).bot_switch(messages['group_id'])
        if bot_switch is None or len(bot_switch) == 0:
            if arg[0] == '/on' and is_admin:
                Database(config).bot_switch(messages['group_id'], 1)
            text = "Bot started successfully."
        else:
            bot_switch = bot_switch[0][1]
    except NameError:
        bot_switch = '0'
        traceback.print_exc()
        pass
    if bot_switch == '0':
        if arg[0] == '/on' and is_admin:
            Database(config).bot_switch(messages['group_id'], 1)
            text = "Bot started successfully."
        else:
            text = None
        return text
    elif bot_switch == '1':
        if arg[0] == '/on' and is_admin:
            text = "Bot is running."
        elif arg[0] == '/off' and is_admin:
            Database(config).bot_switch(messages['group_id'], 0)
            text = "Bot is off."
        elif arg[0] == '/help':
            text = "这是一个帮助列表<Response [200]>"
        elif arg[0] == '/loli':
            text = "[CQ:image,file={$api_json['imgurl']}]"
        elif arg[0] == '/math':
            if arg_len == 1:
                text = "/math method x y z"
            else:
                data = {}
                if arg_len >= 5:
                    try:
                        data['z'] = arg[4]
                    except NameError:
                        pass
                if arg_len >= 4:
                    try:
                        data['y'] = arg[3]
                    except NameError:
                        pass
                if arg_len >= 3:
                    try:
                        data['x'] = arg[2]
                    except NameError:
                        pass
                if arg_len >= 2:
                    try:
                        data['m'] = arg[1]
                    except NameError:
                        pass
                async with aiohttp.ClientSession() as session:
                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
                    }
                    response = await fetch(session, url="https://api.xiwangly.top/math.php", data=data, headers=header)
                    text = f"{response}"
        elif re.match('_http(s)://', message):
            text = "这是一个???"
        elif re.match('\d{1,3}', message):
            text = "选项"
        elif arg[0] == '/calc':
            import math
            try:
                text = eval(arg_all, {"__builtins__": None}, {"math": math})
            except ArithmeticError:
                text = "计算错误，表达式不合法"
        elif arg[0] == '/uuid':
            import uuid
            if arg_len == 1:
                text = str(uuid.uuid4())
            elif arg_len == 3:
                text = str(uuid.uuid5(arg[1], arg[2]))
        elif arg[0] == '/菜单':
            text = '********************\n\
/菜单 或 /help -帮助\n\
[1]/ping ip\n\
/复读 [format] msg(admin)\n\
/start - 开始\n\
[2]/来份萝莉 或 /loli - 发送随机二次元图片\n\
[3]/uuid - 生成UUID\n\
/dwz url - 生成短网址\n\
/m msg - 智能聊天（实验）\n\
/yiyan - 随机一言\n\
/info - 信息\n\
/dic question answer - 增加dic(admin)\n\
/math [x] [y] [z] method - 数学计算\n\
/xuid id - 查询xbox xuid\n\
/fileupload url [name] - 文件上传(admin)\n\
/签到 或 /check_in - 每日签到\n\
/gold user(object) number - 增加金币(admin)\n\
注：[]表示参数可选，部分命令可通过[]的数字简化选择\n\
********************'
        else:
            text = None
        return text


async def main():
    config = {...}  # 配置信息
    messages = {...}  # 消息内容

    text = await chat_thesaurus(messages, config)
    print(text)


if __name__ == '__main__':
    asyncio.run(main())
