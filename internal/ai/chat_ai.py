# noinspection PyPackageRequirements
import aisuite
from internal.ai.ChatHotManager import ChatHotManager
from internal.ai.MemoryManager import MemoryManager

chat_hot_manager = ChatHotManager()
memory_manager = MemoryManager()


async def chat_ai(messages):
    from internal.config import config
    client = aisuite.Client()

    client.configure({config["aisuite"]["provider"]: {
        "api_key": config["aisuite"]["api_key"],
        "base_url": config["aisuite"]["base_url"],
    }})

    model = config["aisuite"]["model"]
    group_id = messages['group_id']

    should_respond = await chat_hot_manager.get_hot(group_id)
    print(f"should_respond: {should_respond}")
    # if not should_respond:
    #     return None

    await memory_manager.update_memory(group_id, messages['message'])
    memory = await memory_manager.get_memory(group_id)

    ai_messages = [
        {"role": "system", "content": '你的名字叫希望酱,你现在处于一个QQ群聊之中,作为博学多识的可爱群员,不要故意装可爱卖萌,而是更自然,注意少使用标点符号,热心解答各种问题和高强度水群记住你说的话要尽量的简洁但具有情感,不要长篇大论,一句话不宜超过五十个字但实际回复可以超过。'},
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

    await memory_manager.merge_and_update_memory(group_id, response.choices[0].message.content)
    await chat_hot_manager.increment_hot(group_id)
    return response.choices[0].message.content
