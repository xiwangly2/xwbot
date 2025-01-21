from sqlalchemy import create_engine

from internal.config import config
from internal.database.models.logs import Logs
from internal.database.models.pic import Pic
from internal.database.models.switch import Switch
from internal.format_output import print_error

try:
    # 根据配置信息创建数据库引擎
    if config['sql']['type'] == 'sqlite3':
        engine = create_engine(config['sql']['sqlite3']['dsn'] or f"sqlite:///{config['sql']['sqlite3']['path']}",
                               pool_pre_ping=True)
    elif config['sql']['type'] == 'mysql':
        ssl_config = {'ssl': {'ca': config['sql']['mysql']['ca_path'], 'key': config['sql']['mysql']['key_path'],
                              'cert': config['sql']['mysql']['cert_path']}} if \
            config['sql']['mysql']['ssl_mode'] != 'disable' else {}
        engine = create_engine(config['sql']['mysql']['dsn'] or
                               f"mysql+pymysql://{config['sql']['mysql']['username']}:{config['sql']['mysql']['password']}@{config['sql']['mysql']['host']}:{config['sql']['mysql']['port']}/{config['sql']['mysql']['database']}",
                               pool_pre_ping=True, connect_args=ssl_config)
    elif config['sql']['type'] == 'postgres':
        ssl_args = f"?sslmode={config['sql']['postgres']['ssl_mode']}&sslrootcert={config['sql']['postgres']['ca_path']}&sslcert={config['sql']['postgres']['cert_path']}&sslkey={config['sql']['postgres']['key_path']}" if \
            config['sql']['postgres']['ssl_mode'] in ['require', 'verify-ca', 'verify-full'] else ""
        if config['sql']['postgres']['srv']:
            # noinspection DuplicatedCode
            engine = create_engine(config['sql']['postgres']['dsn'] or
                                   f"postgresql+psycopg2srv://{config['sql']['postgres']['username']}:{config['sql']['postgres']['password']}@{config['sql']['postgres']['host']}:{config['sql']['postgres']['port']}/{config['sql']['postgres']['database']}{ssl_args}",
                                   pool_pre_ping=True)
        else:
            # noinspection DuplicatedCode
            engine = create_engine(config['sql']['postgres']['dsn'] or
                                   f"postgresql+psycopg2://{config['sql']['postgres']['username']}:{config['sql']['postgres']['password']}@{config['sql']['postgres']['host']}:{config['sql']['postgres']['port']}/{config['sql']['postgres']['database']}{ssl_args}",
                                   pool_pre_ping=True)
    else:
        engine = None
        print_error("不支持的数据库类型")

    # 创建所有未在数据库中创建的表
    Pic.metadata.create_all(engine)
    Logs.metadata.create_all(engine)
    Switch.metadata.create_all(engine)

except Exception as e:
    print_error(f"连接数据库失败: {e}")
