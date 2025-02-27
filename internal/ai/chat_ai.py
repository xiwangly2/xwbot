import multiprocessing
import time
from multiprocessing import Process, Queue

import aisuite as ai


def _generate_response(messages, message):
    """生成 AI 回复"""
    from internal.config import config
    client = ai.Client()
    client.configure({config["aisuite"]["provider"]: {
        "api_key": config["aisuite"]["api_key"],
        "base_url": config["aisuite"]["base_url"],
    }})

    model = config["aisuite"]["model"]
    max_memory_lines = 20

    # 读取现有记忆
    try:
        with open('memory.txt', 'r', encoding='utf-8') as f:
            memory_lines = f.readlines()
    except FileNotFoundError:
        memory_lines = []

    # 添加新记录（转义单引号）
    new_message = message.replace("'", "\\'")
    new_line = f"time:'{messages['time']}',user_id:'{messages['user_id']}',message:'{new_message}'\n"
    memory_lines.append(new_line)

    # 控制记忆长度（按行截断）
    if len(memory_lines) > max_memory_lines:
        memory_lines = memory_lines[-max_memory_lines:]

    # 控制记忆长度（按字符截断）
    if len(''.join(memory_lines)) > 1000:
        memory_lines = memory_lines[-1:]

    # 写入记忆文件
    with open('memory.txt', 'w', encoding='utf-8') as f:
        f.writelines(memory_lines)

    # 构造记忆上下文
    memory_str = ''.join(memory_lines)

    ai_messages = [
        {"role": "system",
         "content": '你现在处于QQ群聊中，作为博学可爱的群员，自然交流，避免刻意卖萌，回答需简洁（50字内最佳）但富有情感。'},
        {"role": "user", "content": f"记忆上下文:\n{memory_str}"},
        {"role": "user", "content": f"新消息:\n{messages}"},
    ]

    try:
        if messages['self_id'] == messages['user_id']:
            return None

        response = client.chat.completions.create(
            model=model,
            messages=ai_messages,
            temperature=0.75
        )
        return response.choices[0].message.content
    except Exception:
        if config['debug']:
            import traceback
            traceback.print_exc()
        return None


class ChatAIProcess:
    def __init__(self):
        self.heat_value = 0
        self.last_update_time = time.time()
        self.input_queue = Queue()  # 用于接收消息
        self.output_queue = Queue()  # 用于发送回复

    def run(self):
        """独立进程的主逻辑"""
        while True:
            print(f"chat_ai 进程正在运行，当前热度值：{self.heat_value}")
            try:
                # 非阻塞获取消息
                messages, message = self.input_queue.get_nowait()
                self._update_heat_value(messages, message)
                if self.heat_value > 0 or f"[CQ:at,qq={messages['self_id']}]" in message:
                    response = _generate_response(messages, message)
                    self.output_queue.put(response)
            except multiprocessing.queues is None:
                # 如果没有消息，跳过处理
                pass

            # 更新时间衰减
            self._update_heat_value(None, {})

            # 避免 CPU 占用过高
            time.sleep(0.1)

    def _update_heat_value(self, messages, message):
        """更新热度值"""
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        # 热度衰减（每秒钟减少 1）
        self.heat_value = max(0, int(self.heat_value - 1 * time_elapsed))

        # 如果被@，增加热度值
        if messages is not None and f"[CQ:at,qq={messages['self_id']}]" in message:
            self.heat_value = min(5000, self.heat_value + 500)


# 全局变量，用于管理 ChatAIProcess 实例和 Process 对象
chat_ai_instance = None
chat_ai_process = None


def start_chat_ai_process():
    """启动 chat_ai 进程"""
    global chat_ai_instance, chat_ai_process
    if chat_ai_process is None or not chat_ai_process.is_alive():
        chat_ai_instance = ChatAIProcess()  # 创建 ChatAIProcess 实例
        chat_ai_process = Process(target=chat_ai_instance.run)  # 创建 Process 对象
        chat_ai_process.start()
        print("chat_ai 进程已启动。")
    return chat_ai_instance  # 返回 ChatAIProcess 实例


def stop_chat_ai_process():
    """停止 chat_ai 进程"""
    global chat_ai_process
    if chat_ai_process is not None:
        chat_ai_process = None
        print("chat_ai 进程已停止。")
