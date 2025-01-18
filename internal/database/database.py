from internal.config import config


class Database:
    def __init__(self):
        self.db_handler = None
        if config['select_database'] == 'mysql':
            from internal.database.mysql_handler import MySQLDatabase
            self.db_handler = MySQLDatabase()
        elif config['select_database'] == 'sqlite':
            from internal.database.sqlite_handler import SQLiteDatabase
            self.db_handler = SQLiteDatabase()
        elif config['select_database'] == 'postgresql':
            from internal.database.postgresql_handler import PostgreSQLDatabase
            self.db_handler = PostgreSQLDatabase()
        elif config['select_database'] == 'mongo':
            from internal.database.mongo_handler import MongoDatabase
            self.db_handler = MongoDatabase()
        else:
            raise ValueError("Unsupported database type")

    def connect(self):
        if self.db_handler:
            self.db_handler.__init__()
        else:
            raise ValueError("Database handler is not initialized")
