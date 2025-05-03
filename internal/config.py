import yaml


def load_config(file_path):
    """加载配置文件并提供默认值"""
    with open(file_path, 'r', encoding='utf-8') as f:
        xwbot_config = yaml.safe_load(f)

    # 提供默认值
    xwbot_config.setdefault('host', 'localhost')
    xwbot_config.setdefault('port', '6700')
    xwbot_config.setdefault('access_token', '')
    xwbot_config.setdefault('debug', False)
    xwbot_config.setdefault('write_log', True)
    xwbot_config.setdefault('auto_reconnect', False)
    xwbot_config.setdefault('save_method', 'local')
    xwbot_config.setdefault('local_save_path', './downloads')
    xwbot_config.setdefault('minio', {
        'endpoint': '',
        'access_key': '',
        'secret_key': '',
        'secure': 'true',
        'bucket_name': ''
    })
    xwbot_config.setdefault('admin', [])
    xwbot_config.setdefault('sql', {
        'type': 'sqlite3',
        'sqlite3': {
            'path': 'data.db',
            'connect_args': {}
        },
        'mysql': {
            'username': '',
            'password': '',
            'host': 'localhost',
            'port': 3306,
            'database': '',
            'connect_args': {}
        },
        'postgres': {
            'username': '',
            'password': '',
            'host': 'localhost',
            'port': 5432,
            'database': '',
            'connect_args': {}
        },
        'dsn': {
            'value': 'sqlite+pysqlite:///:memory:',
            'connect_args': {}
        }
    })
    xwbot_config.setdefault('aisuite', {
        'provider': 'openai',
        'api_key': '',
        'model': '',
        'base_url': ''
    })

    return xwbot_config


# 加载配置
config = load_config('config/config.yml')
