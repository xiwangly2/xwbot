import os
import yaml


xwbot_config = None


# 异步函数，用于加载配置
async def load_config():
    global xwbot_config
    if xwbot_config is None:  # 如果xwbot_config还未加载
        if os.path.exists('config/config.yml'):
            with open('config/config.yml', 'r', encoding='utf-8') as f:
                xwbot_config = yaml.load(f.read(), Loader=yaml.FullLoader)
        else:
            print_warning("Warning: No configuration file found, the example file will be used.")
            with open('config/config_example.yml', 'r', encoding='utf-8') as f:
                xwbot_config = yaml.load(f.read(), Loader=yaml.FullLoader)
    return xwbot_config
