# import re

# message = '/calc 1111 3+33'
# result = re.match('/calc (.*)', message).group(1)
# print(result)

import re

message = "[CQ:reply,id=-1519369564][CQ:at,qq=1334850101] /savepic 群除我佬.jpg"
pattern = r'\[CQ:reply,id=(-?\d+)\]'
matches = re.findall(pattern, message)

if matches:
    text = matches[0]  # 提取第一个匹配到的 id
    text = {
        'auto_escape': False,
        'text_list': ['***.jpg', message, "reply id = " + text]
    }
    print(text)
else:
    print("没有找到匹配的 id。")