import re
import html

messages = {
    'message': '[CQ:at,qq=2946692758] /on 1122'
}

# 消息文本内容
if messages['message']:
    message = html.unescape(messages['message'])
    # 按空格分隔参数
    arg = re.split(r'\s', message)
    # 计算参数数量
    arg_len = len(arg)
else:
    message = None
    arg = ['']
    arg_len = 0

# 捕获一个命令后的所有内容
if arg_len > 1:
    match = re.match(arg[0] + ' (.*)', message)
    if match:
        arg_all = match.group(1)
    else:
        arg_all = None
else:
    arg_len = 1
    arg_all = None

print(arg)
print(arg_all)
