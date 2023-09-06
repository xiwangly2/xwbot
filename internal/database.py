# 暂时弃用


class Database:
    def __init__(self, global_config):
        if global_config['select_database'] == 'mysql':
            from internal.database.mysql_handler import Database
        elif global_config['select_database'] == 'sqlite':
            pass
        elif global_config['select_database'] == 'mongo':
            pass
        elif global_config['select_database'] == 'postgresql':
            pass
        else:
            pass

    def connect(self, global_config):
        pass
