import aisuite as ai

from internal.ai.ChatHotManager import ChatHotManager
from internal.ai.MemoryManager import MemoryManager

chat_hot_manager = ChatHotManager()
memory_manager = MemoryManager()


async def chat_ai(messages):
    from internal.config import config
    client = ai.Client()

    client.configure({config["aisuite"]["provider"]: {
        "api_key": config["aisuite"]["api_key"],
        "base_url": config["aisuite"]["base_url"],
    }})

    model = config["aisuite"]["model"]
    group_id = messages.get('group_id')
    if not group_id:
        return None

    # should_respond = await chat_hot_manager.get_hot(group_id)
    # if not should_respond:
    #     return None

    await memory_manager.update_memory(group_id, messages['message'])
    memory = await memory_manager.get_memory(group_id)

    ai_messages = [
        {"role": "system", "content": "你扮演QQ群里的一只猫娘，我现在把完整的接收消息参数给你，你需要对消息进行回复。"},
        {"role": "user", "content": f"messages: {memory}"},
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=ai_messages,
            temperature=0.75
        )
        if messages['self_id'] == messages['user_id']:
            return None
    except Exception:
        if config['debug']:
            import traceback
            traceback.print_exc()
        return None

    await memory_manager.update_memory(group_id, response.choices[0].message.content)
    # await chat_hot_manager.increment_hot(group_id)
    return response.choices[0].message.content
