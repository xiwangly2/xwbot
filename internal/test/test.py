import re

message = '/calc 1111 3+33'
result = re.match('/calc (.*)', message).group(1)
print(result)
