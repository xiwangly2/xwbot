from sqlalchemy import create_engine
from internal.config import config
from internal.database.models.logs import Logs
from internal.database.models.pic import Pic
from internal.database.models.switch import Switch
from internal.format_output import print_error


def _handle_sqlite3(sql_config):
    """处理SQLite3数据库配置"""
    return (
        sql_config.get('dsn') or f"sqlite:///{sql_config['path']}",
        {}
    )


def _handle_mysql(sql_config):
    """处理MySQL数据库配置"""
    ssl_args = {}
    if sql_config['ssl_mode'] != 'disable':
        ssl_args = {
            'ssl': {
                'ca': sql_config['ca_path'],
                'key': sql_config['key_path'],
                'cert': sql_config['cert_path']
            }
        }

    return (
        sql_config.get('dsn') or (
            f"mysql+pymysql://{sql_config['username']}:"
            f"{sql_config['password']}@{sql_config['host']}:"
            f"{sql_config['port']}/{sql_config['database']}"
        ),
        ssl_args
    )


def _handle_postgres(sql_config):
    """处理PostgreSQL数据库配置"""
    ssl_params = []
    if sql_config['ssl_mode'] in ['require', 'verify-ca', 'verify-full']:
        ssl_params.extend([
            f"sslmode={sql_config['ssl_mode']}",
            f"sslrootcert={sql_config['ca_path']}",
            f"sslcert={sql_config['cert_path']}",
            f"sslkey={sql_config['key_path']}"
        ])

    driver = 'psycopg2srv' if sql_config['srv'] else 'psycopg2'
    ssl_suffix = f"?{'&'.join(ssl_params)}" if ssl_params else ""

    return (
        sql_config.get('dsn') or (
            f"postgresql+{driver}://{sql_config['username']}:"
            f"{sql_config['password']}@{sql_config['host']}:"
            f"{sql_config['port']}/{sql_config['database']}"
            f"{ssl_suffix}"
        ),
        {}
    )


# 数据库类型与处理函数的映射
DB_HANDLERS = {
    'sqlite3': (_handle_sqlite3, 'sqlite3'),
    'mysql': (_handle_mysql, 'mysql'),
    'postgres': (_handle_postgres, 'postgres')
}

engine = None

try:
    db_type = config['sql']['type']
    if db_type not in DB_HANDLERS:
        raise ValueError(f"不支持的数据库类型: {db_type}")

    handler, config_key = DB_HANDLERS[db_type]
    dsn, connect_args = handler(config['sql'][config_key])

    engine = create_engine(dsn, pool_pre_ping=True, connect_args=connect_args)

    # 统一创建所有表
    for model in [Pic, Logs, Switch]:
        model.metadata.create_all(engine)

except Exception as e:
    print_error(f"数据库连接失败: {str(e)}")
    engine = None
