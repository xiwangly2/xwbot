import datetime
import json
import traceback

from pymongo import MongoClient

# 导入自己写的模块
from internal.config import config


class MongoDatabase:
    def __init__(self):
        try:
            # 建立与MongoDB的连接
            self.client = MongoClient(
                uri=config['mongodb']['uri']
            )
            self.db = self.client[config['mongodb']['database']]  # 选择数据库
        except Exception:
            print("Could not connect to MongoDB")
            traceback.print_exc()

    def chat_logs(self, messages=None):
        try:
            collection = self.db['logs']  # 选择集合

            messages = json.dumps(messages, ensure_ascii=False)

            # 插入文档
            document = {
                'json': messages,
                'time': datetime.datetime.now()
            }
            result = collection.insert_one(document)
            print("插入的文档ID：", result.inserted_id)
        except Exception:
            traceback.print_exc()

    def bot_switch(self, group_id='0', switch=None):
        try:
            collection = self.db['switch']  # 选择集合

            if switch is not None:
                # 插入或更新文档
                document = {
                    'group_id': group_id,
                    'switch': switch,
                    'time': datetime.datetime.now()
                }
                collection.replace_one({'group_id': group_id}, document, upsert=True)
            else:
                # 查询文档
                result = collection.find_one({'group_id': group_id})
                return result
        except Exception:
            traceback.print_exc()
