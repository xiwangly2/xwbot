import datetime
import json
import traceback
import pymysql

class Database():
    def __init__(self, config):
        self.config = config
        # 打开数据库连接
        try:
            self.db = pymysql.connect(host=config['mysql']['host'], user=config['mysql']['user'], 
                             password=config['mysql']['password'], database=config['mysql']['database'])
        except Exception:
            print("Could not connect to MySQL")
        self.db.begin()
    
    def chat_logs(self, messages = None):    
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = self.db.cursor()
            
            messages = json.dumps(messages, ensure_ascii=False)
            
            # 使用 execute()  方法执行 SQL 查询
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(f"INSERT INTO `{self.config['mysql']['database']}`.`logs` (`id`, `json`, `time`) VALUES (null, '{messages}', '{date}')")
            
            # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchall()
            
            # print(data)
            
            # 提交
            self.db.commit()
        except Exception:
            self.db.rollback()
            traceback.print_exc()
    
    def __del__(self):
        # 关闭数据库连接
        self.db.close()
        
# Database(config).chat_logs(messages)