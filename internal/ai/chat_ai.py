import time

# noinspection PyPackageRequirements
import aisuite as ai

# 全局变量存储热度值
heat_value = 0
last_update_time = time.time()


async def chat_ai(messages, message):
    from internal.config import config
    global heat_value, last_update_time

    client = ai.Client()
    client.configure({config["aisuite"]["provider"]: {
        "api_key": config["aisuite"]["api_key"],
        "base_url": config["aisuite"]["base_url"],
    }})

    model = config["aisuite"]["model"]
    max_memory_lines = 20  # 可配置为从config读取

    # 更新热度值
    current_time = time.time()
    time_elapsed = current_time - last_update_time
    last_update_time = current_time

    # 热度衰减（每秒钟减少 1）
    heat_value = max(0, int(heat_value - 1 * time_elapsed))

    # 如果被@，增加热度值
    if f"[CQ:at,qq={messages['self_id']}]" in message:
        heat_value = min(50, heat_value + 1)  # 热度值上限为 50

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

        # 根据热度值决定是否回复
        if heat_value > 0 or f"[CQ:at,qq={messages['self_id']}]" in message:
            response = client.chat.completions.create(
                model=model,
                messages=ai_messages,
                temperature=0.75
            )
            return response.choices[0].message.content
        else:
            print(f"热度值过低，不回复: {heat_value}")
            return None
    except Exception:
        if config['debug']:
            import traceback
            traceback.print_exc()
        return None
