from asyncio import Lock


class MemoryManager:
    def __init__(self):
        self.short_term_memory = {}
        self.long_term_memory = {}
        self.lock = Lock()

    async def update_memory(self, group_id, new_message):
        async with self.lock:
            if group_id not in self.short_term_memory:
                self.short_term_memory[group_id] = []
            self.short_term_memory[group_id].append(new_message)
            if len(self.short_term_memory[group_id]) > 100:
                self.long_term_memory[group_id] = self.long_term_memory.get(group_id, "") + " ".join(
                    self.short_term_memory[group_id][:50])
                self.short_term_memory[group_id] = self.short_term_memory[group_id][50:]

    async def get_memory(self, group_id):
        async with self.lock:
            long_term = self.long_term_memory.get(group_id, "")
            short_term = " ".join(self.short_term_memory.get(group_id, []))
            return long_term + short_term

    async def clear_memory(self, group_id, memory_type):
        async with self.lock:
            if memory_type == 'short':
                self.short_term_memory[group_id] = []
            elif memory_type == 'long':
                self.long_term_memory[group_id] = ""
