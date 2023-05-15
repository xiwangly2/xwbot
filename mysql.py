import datetime
import json
import traceback

import pymysql
from pymysql.converters import escape_string


class ConnectMysql():
    def __init__(self, config):
        self.config = config
        # 打开数据库连接
        try:
            self.db = pymysql.connect(host=config['mysql']['host'], user=config['mysql']['user'],
                                      password=config['mysql']['password'], database=config['mysql']['database'])
        except Exception:
            print("Could not connect to MySQL")
            traceback.print_exc()
        # 启用事务
        self.db.begin()

    def __del__(self):
        # 关闭数据库连接
        self.db.close()


class Database(ConnectMysql):
    def chat_logs(self, messages=None):
        try:
            cursor = self.db.cursor()

            messages = json.dumps(messages, ensure_ascii=False)
            messages = escape_string(messages)

            # 插入 SQL 记录
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                f"INSERT INTO `logs` (`id`, `json`, `time`) VALUES (null, '{messages}', '{date}')")

            # 提交
            self.db.commit()
        except Exception:
            # 回滚
            self.db.rollback()
            traceback.print_exc()

    def bot_switch(self, group_id='0', switch=None):
        try:
            cursor = self.db.cursor()
            if switch != None:
                # 插入 SQL 记录
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    f"REPLACE INTO `switch` (`group_id`, `switch`, `time`) VALUES ('{group_id}', '{switch}', '{date}')")
            else:
                cursor.execute(
                    f"select * from `switch` where `group_id` = '{group_id}'")
                return cursor.fetchall()
            # 提交
            self.db.commit()
        except Exception:
            # 回滚
            self.db.rollback()
            traceback.print_exc()
