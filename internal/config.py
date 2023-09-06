import asyncio
import os

import yaml



# 导入自己写的模块
from internal.functions import *
from internal.functions import print_warning


# 异步函数，用于加载配置
async def load_config():
    global global_config
    if 'global_config' not in locals():  # 如果global_config还未加载
        if os.path.exists('config/config.yml'):
            with open('config/config.yml', 'r', encoding='utf-8') as f:
                global_config = yaml.load(f.read(), Loader=yaml.FullLoader)
        else:
            print_warning("Warning: No configuration file found, the example file will be used.")
            with open('config/config_example.yml', 'r', encoding='utf-8') as f:
                global_config = yaml.load(f.read(), Loader=yaml.FullLoader)
    return global_config

# 判断变量是否存在，如果不存在就初始化
if 'global_config' not in locals():
    global_config = asyncio.run(load_config())

