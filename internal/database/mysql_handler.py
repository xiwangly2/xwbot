import asyncio
import datetime
import json
import time
import traceback

import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.converters import escape_string



class Database:
    def __init__(self, global_config):
        self.global_config = global_config
        # 创建数据库连接池
        try:
            self.pool = PooledDB(
                creator=pymysql,  # 使用 PyMySQL 作为数据库连接库
                maxconnections=10,  # 设置最大连接数
                host=global_config['mysql']['host'], user=global_config['mysql']['user'],
                password=global_config['mysql']['password'], database=global_config['mysql']['database']  # 将配置参数传递给连接池
            )
        except Exception:
            print("Could not create database connection pool")
            if self.global_config['debug']:
                traceback.print_exc()

    def chat_logs(self, messages=None):
        try:
            conn = self.pool.connection()  # 从连接池获取连接
            cursor = conn.cursor()

            messages = json.dumps(messages, ensure_ascii=False)
            messages = escape_string(messages)

            # 插入 SQL 记录
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                f"INSERT INTO `logs` (`id`, `json`, `time`) VALUES (null, '{messages}', '{date}')")

            conn.commit()  # 提交事务
            cursor.close()
            conn.close()  # 将连接放回连接池
        except Exception:
            if self.global_config['debug']:
                traceback.print_exc()

    def bot_switch(self, group_id='0', switch=None):
        try:
            conn = self.pool.connection()  # 从连接池获取连接
            cursor = conn.cursor()

            if switch is not None:
                # 插入 SQL 记录
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    f"REPLACE INTO `switch` (`group_id`, `switch`, `time`) VALUES ('{group_id}', '{switch}', '{date}')")
            else:
                cursor.execute(
                    f"SELECT * FROM `switch` WHERE `group_id` = '{group_id}'")
                return cursor.fetchall()

            conn.commit()  # 提交事务
            cursor.close()
            conn.close()  # 将连接放回连接池
        except Exception:
            if self.global_config['debug']:
                traceback.print_exc()
