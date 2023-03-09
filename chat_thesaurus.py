import math
import re
import traceback
import requests
from mysql import Database

# 判断QQ号是否在管理员列表里
def f_is_admin(target_id, config):
    if f"{target_id}" in config['admin']:
        return True
    else:
        return False

def chat_thesaurus(messages, config):
    # 消息文本内容
    message = messages['message']
    # 按空格分隔参数
    arg = re.split('\s', message)
    # 计算参数数量
    arg_len = len(arg)
    # 捕获一个命令后的所有内容
    if arg_len > 1:
        try:
            arg_all = re.match(arg[0]+' (.*)', message).group(1)
        except Exception:
            pass
    is_admin = f_is_admin(messages['user_id'], config)
    try:
        # 查询开关
        bot_switch = Database(config).bot_switch(messages['group_id'])
        if bot_switch == None:
            bot_switch = '0'
        else:
            bot_switch = bot_switch[0][1]
    except Exception:
        bot_switch = '0'
        traceback.print_exc()
        pass
    if bot_switch == '0':
        if arg[0] == '/on' and is_admin:
            Database(config).bot_switch(messages['group_id'], 1)
            text = "Bot started successfully"
        else:
            text = None
        return text
    elif bot_switch == '1':
        if arg[0] == '/on' and is_admin:
            text = "Bot is running"
        elif arg[0] == '/off' and is_admin:
            Database(config).bot_switch(messages['group_id'], 0)
            text = "Bot is off"
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
                    try: data['z'] = arg[4]
                    except: pass
                if arg_len >= 4:
                    try: data['y'] = arg[3]
                    except: pass
                if arg_len >= 3:
                    try: data['x'] = arg[2]
                    except: pass
                if arg_len >= 2:
                    try: data['m'] = arg[1]
                    except: pass
                header = {
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
                    }
                response = requests.post(url = "https://api.xiwangly.top/math.php", data = data, headers = header).text
                text = f"{response}"
        elif re.match('_http(s)\:\/\/', message):
            text = "这是一个???"
        elif re.match('\d{1,3}', message):
            text = "选项"
        elif arg[0] == '/calc':
            # 计算器pymysql.err.OperationalError: (1054, "Unknown column '589394954' in 'where clause'")
            try:
                text = eval(arg_all, {"__builtins__":None},{"math": math})
            except Exception:
                text = "计算错误，表达式不合法"
        else:
            text = None
        return text