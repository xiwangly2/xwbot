from sqlalchemy import create_engine

from internal.config import config
from internal.database.models.logs import Logs
from internal.database.models.pic import Pic
from internal.database.models.switch import Switch
from internal.format_output import print_error


def _handle_dsn(sql_config):
    """处理DSN数据库配置"""
    return sql_config, {}


def _handle_sqlite3(sql_config):
    """处理SQLite3数据库配置"""
    return f"sqlite:///{sql_config['path']}", sql_config['connect_args']


def _handle_mysql(sql_config):
    """处理MySQL数据库配置"""
    return f"mysql+pymysql://{sql_config['username']}:{sql_config['password']}@{sql_config['host']}:{sql_config['port']}/{sql_config['database']}", sql_config['connect_args']


def _handle_postgres(sql_config):
    """处理PostgreSQL数据库配置"""
    driver = 'psycopg2srv' if sql_config['srv'] else 'psycopg2'
    host_port = f"{sql_config['host']}" if sql_config['srv'] else f"{sql_config['host']}:{sql_config['port']}"
    return f"postgresql+{driver}://{sql_config['username']}:{sql_config['password']}@{host_port}/{sql_config['database']}", sql_config['connect_args']


# 数据库类型与处理函数的映射
DB_HANDLERS = {
    'dsn': (_handle_dsn, 'dsn'),
    'sqlite3': (_handle_sqlite3, 'sqlite3'),
    'mysql': (_handle_mysql, 'mysql'),
    'postgres': (_handle_postgres, 'postgres'),
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
