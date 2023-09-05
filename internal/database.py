# 暂时弃用


class Database:
    def __init__(self, xwbot_config):
        if xwbot_config['select_database'] == 'mysql':
            pass
        elif xwbot_config['select_database'] == 'sqlite':
            pass
        elif xwbot_config['select_database'] == 'mongo':
            pass
        elif xwbot_config['select_database'] == 'postgresql':
            pass
        else:
            pass

    def connect(self, xwbot_config):
        pass
