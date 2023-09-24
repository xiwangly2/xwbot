import os
import yaml


# 机器人配置信息
if os.path.exists('config/config.yml'):
    with open('config/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
else:
    from colorama import Fore, Style

    # 输出黄色警告消息的函数
    def print_warning(message):
        print(Fore.YELLOW + message + Style.RESET_ALL)
    
    print_warning("Warning: No configuration file found, the example file will be used.")
    with open('config/config_example.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)