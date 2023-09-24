import hashlib
import json
import traceback
from datetime import datetime
from dbutils.pooled_db import PooledDB
import pymysql
from pymysql.converters import escape_string
# 导入自己写的模块
from internal.config import config

class Database:
    def __init__(self):
        # 创建数据库连接池
        try:
            self.pool = PooledDB(
                creator=pymysql,  # 使用 PyMySQL 作为数据库连接库
                maxconnections=10,  # 设置最大连接数
                host=config['mysql']['host'], user=config['mysql']['user'],
                                      password=config['mysql']['password'], database=config['mysql']['database'] # 将配置参数传递给连接池
            )
        except Exception:
            print("Could not create database connection pool")
            if config['debug']:
                traceback.print_exc()

    def chat_logs(self, messages=None):
        try:
            conn = self.pool.connection()  # 从连接池获取连接
            cursor = conn.cursor()

            messages = json.dumps(messages, ensure_ascii=False)
            messages = escape_string(messages)

            # 插入 SQL 记录
            date = datetime.now()
            cursor.execute(
                f"INSERT INTO `logs` (`id`, `json`, `time`) VALUES (null, '{messages}', '{date}')")

            conn.commit()  # 提交事务
            cursor.close()
            conn.close()  # 将连接放回连接池
        except Exception:
            if config['debug']:
                traceback.print_exc()

    def bot_switch(self, group_id='0', switch=None):
        try:
            conn = self.pool.connection()  # 从连接池获取连接
            cursor = conn.cursor()

            if switch is not None:
                # 插入 SQL 记录
                date = datetime.now()
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
            if config['debug']:
                traceback.print_exc()

    def image_exists(self, sha256_hash, md5_hash):
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT `id` FROM `pic` WHERE `sha256` = '{sha256_hash}' OR `md5` = '{md5_hash}'"
            )

            result = cursor.fetchone()
            return result is not None

        except Exception:
            if config['debug']:
                traceback.print_exc()

    def save_image(self, name, image_data):
        try:
            # 计算图片的SHA-256和MD5哈希值
            sha256_hash = hashlib.sha256(image_data).hexdigest()
            md5_hash = hashlib.md5(image_data).hexdigest()

            # 先检查图片是否已存在
            if self.image_exists(sha256_hash, md5_hash):
                return "Image already exists in the database."
            else:
                conn = self.pool.connection()
                cursor = conn.cursor()

                # 插入图片信息到数据库
                cursor.execute(
                    f"INSERT INTO `pic` (`name`, `bin`, `sha256`, `md5`) VALUES ('{name}', %s, '{sha256_hash}', '{md5_hash}')",
                    (image_data,)
                )

            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if config['debug']:
                traceback.print_exc()

    def rename_image(self, old_name, new_name):
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()

            cursor.execute(
                f"UPDATE `pic` SET `name` = '{new_name}' WHERE `name` = {old_name}"
            )

            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if config['debug']:
                traceback.print_exc()

    def delete_image(self, name):
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()

            cursor.execute(
                f"DELETE FROM `pic` WHERE `name` = {name}"
            )

            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if config['debug']:
                traceback.print_exc()

    def query_image(self, name):
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT `id`, `name`, `bin` FROM `pic` WHERE `name` = {name}"
            )

            result = cursor.fetchone()
            if result:
                image_info = {
                    "id": result[0],
                    "name": result[1],
                    "bin": result[2]
                }
                return json.dumps(image_info, ensure_ascii=False)

            cursor.close()
            conn.close()
        except Exception:
            if config['debug']:
                traceback.print_exc()