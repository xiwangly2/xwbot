import re

def parse_dic_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    text = re.sub(r'\n\/\/.+', '', text)
    dic = re.split(r'\n\n', text)

    dic_qa = {}
    for entry in dic:
        dic_q = entry.split('\n', 1)
        key = dic_q[0].strip()
        value = dic_q[1].strip() if len(dic_q) > 1 else ''
        dic_qa[key] = value

    return dic_qa


def replace_variables(message, variables):
    for key, value in variables.items():
        placeholder = '%' + key + '%'
        message = message.replace(placeholder, value)
    return message


# 使用示例
dic_file = 'dic.txt'
dic_qa = parse_dic_file(dic_file)

variables = {
    'QQ': str(messages['user_id']),
    '群号': str(messages['group_id']),
    '主人': administrator_id,
    '管理员': '',
    'GroupName': '',
    'Robot': str(messages['self_id']),
    'Type': str(messages['post_type']),
    'Msgbar': str(messages['message_id']),
    'Time': str(messages['time']),
    'UinName': messages['sender']['nickname'],
    'Title': messages['sender']['title'],
    'Code': messages['sender']['user_id'],
    'Uin': messages['sender']['user_id'],
    '参数-1': messages['message'],
    # '参数0': var0,
    # '参数1': var1,
    # '参数2': var2,
    # '参数3': var3,
    # '参数4': var4,
    # '参数5': var5,
    # '参数6': var6,
    # '参数7': var7,
    # '参数8': var8,
    # '参数9': var9,
    # '参数10': var10,
    '昵称': messages['sender']['nickname']
}

qrspeed_message = replace_variables(message, variables)
