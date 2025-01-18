import datetime
import json
import sqlite3
import traceback
from sqlite3 import Error

# 导入自己写的模块
from internal.config import config


class SQLiteDatabase:
    def __init__(self):
        # 创建数据库连接
        try:
            self.conn = sqlite3.connect(config['sqlite']['database'])
        except Error:
            print("Could not create SQLite database connection")
            if config['debug']:
                traceback.print_exc()

    def chat_logs(self, messages=None):
        try:
            cursor = self.conn.cursor()

            messages = json.dumps(messages, ensure_ascii=False)

            # 插入 SQL 记录
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO logs (id, json, time) VALUES (null, ?, ?)",
                (messages, date)
            )

            self.conn.commit()  # 提交事务
            cursor.close()
        except Error:
            if config['debug']:
                traceback.print_exc()

    def bot_switch(self, group_id='0', switch=None):
        try:
            cursor = self.conn.cursor()

            if switch is not None:
                # 插入 SQL 记录
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "REPLACE INTO switch (group_id, switch, time) VALUES (?, ?, ?)",
                    (group_id, switch, date)
                )
            else:
                cursor.execute(
                    "SELECT * FROM switch WHERE group_id = ?",
                    (group_id,)
                )
                return cursor.fetchall()

            self.conn.commit()  # 提交事务
            cursor.close()
        except Error:
            if config['debug']:
                traceback.print_exc()
