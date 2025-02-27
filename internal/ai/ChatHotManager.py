import asyncio
from asyncio import Lock
from time import time


class ChatHotManager:
    def __init__(self):
        self.chat_hot = {}
        self.chat_hot_lock = Lock()

    async def get_hot(self, group_id):
        async with self.chat_hot_lock:
            current_time = time()
            chat_hot_data = self.chat_hot.get(group_id)
            if chat_hot_data:
                if current_time - chat_hot_data['usetime'] > 30:
                    chat_hot_data['usetime'] = current_time
                    chat_hot_data['usecount'] = 0
                    self.chat_hot[group_id] = chat_hot_data
                    return False
                elif 0 < chat_hot_data['usecount'] < 2:
                    return True
                return False
            self.chat_hot[group_id] = {'usetime': current_time, 'usecount': 0}
            return False

    async def increment_hot(self, group_id):
        async with self.chat_hot_lock:
            current_time = time()
            chat_hot_data = self.chat_hot.get(group_id)
            if chat_hot_data:
                chat_hot_data['usecount'] += 1
                self.chat_hot[group_id] = chat_hot_data
            else:
                self.chat_hot[group_id] = {'usetime': current_time, 'usecount': 1}
