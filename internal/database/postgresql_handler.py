import hashlib
import json
import traceback
from datetime import datetime
from xmlrpc.client import Boolean

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
# Import your own module
from internal.config import config


class PostgreSQLDatabase:
    def __init__(self):
        # Create a connection pool
        try:
            self.pool = pool.SimpleConnectionPool(
                1, 10,  # min and max connections
                user=config['postgresql']['user'],
                password=config['postgresql']['password'],
                host=config['postgresql']['host'],
                port=config['postgresql']['port'],
                database=config['postgresql']['database']
            )
        except Exception:
            print("Could not create database connection pool")
            if config['debug']:
                traceback.print_exc()

    def chat_logs(self, messages=None):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()

            messages = json.dumps(messages, ensure_ascii=False)

            # Insert SQL record
            date = datetime.now()
            cursor.execute(
                "INSERT INTO logs (id, json, time) VALUES (DEFAULT, %s, %s)",
                (messages, date)
            )

            conn.commit()  # Commit transaction
            cursor.close()
            self.pool.putconn(conn)  # Return connection to pool
        except Exception:
            if config['debug']:
                traceback.print_exc()

    def bot_switch(self, group_id='0', switch=None):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            if switch is not None:
                # Insert or update SQL record
                date = datetime.now()
                cursor.execute(
                    "INSERT INTO switch (group_id, switch, time) VALUES (%s, %s, %s) ON CONFLICT (group_id) DO UPDATE SET switch = EXCLUDED.switch, time = EXCLUDED.time",
                    (group_id, switch, date)
                )
                conn.commit()  # Commit transaction
                cursor.close()
                self.pool.putconn(conn)  # Return connection to pool
                return True
            else:
                cursor.execute(
                    "SELECT switch FROM switch WHERE group_id = %s",
                    (group_id,)
                )
                result = cursor.fetchone()
                cursor.close()
                self.pool.putconn(conn)  # Return connection to pool
                if result:
                    return result['switch'] == '1'
                else:
                    return False
        except Exception:
            if config['debug']:
                traceback.print_exc()
            return False

    def image_exists(self, sha256_hash, md5_hash):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM pic WHERE sha256 = %s OR md5 = %s",
                (sha256_hash, md5_hash)
            )

            result = cursor.fetchone()
            return result is not None

        except Exception:
            if config['debug']:
                traceback.print_exc()

    def save_image(self, name, image_data):
        try:
            # Calculate SHA-256 and MD5 hashes of the image
            sha256_hash = hashlib.sha256(image_data).hexdigest()
            md5_hash = hashlib.md5(image_data).hexdigest()

            # Check if the image already exists
            if self.image_exists(sha256_hash, md5_hash):
                return "Image already exists in the database."
            else:
                conn = self.pool.getconn()
                cursor = conn.cursor()

                # Insert image information into the database
                cursor.execute(
                    "INSERT INTO pic (name, bin, sha256, md5) VALUES (%s, %s, %s, %s)",
                    (name, psycopg2.Binary(image_data), sha256_hash, md5_hash)
                )

            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except Exception:
            if config['debug']:
                traceback.print_exc()

    def rename_image(self, old_name, new_name):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE pic SET name = %s WHERE name = %s",
                (new_name, old_name)
            )

            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except Exception:
            if config['debug']:
                traceback.print_exc()

    def delete_image(self, name):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM pic WHERE name = %s",
                (name,)
            )

            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except Exception:
            if config['debug']:
                traceback.print_exc()

    def query_image(self, name):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute(
                "SELECT id, name, bin FROM pic WHERE name = %s",
                (name,)
            )

            result = cursor.fetchone()
            if result:
                image_info = {
                    "id": result['id'],
                    "name": result['name'],
                    "bin": result['bin']
                }
                return json.dumps(image_info, ensure_ascii=False)

            cursor.close()
            self.pool.putconn(conn)
        except Exception:
            if config['debug']:
                traceback.print_exc()
