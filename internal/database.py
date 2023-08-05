# 暂时弃用
import yaml

class Database:
    def __init__(self, config):
        if config['select_database']  ==  'mysql':
            from internal.database.mysql_handler import Database
        elif config['select_database'] == 'sqlite':
            pass
        elif config['select_database'] == 'mongo':
            pass
        elif config['select_database'] == 'postgresql':
            pass
        else:
            pass
    def connect(self, config):
        pass