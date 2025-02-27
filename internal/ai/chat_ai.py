# noinspection PyPackageRequirements
import aisuite
from internal.config import config


async def chat_ai(messages):
    async def merge_and_update_memory(existing_memories, new_memories):
        ai_messages = [
            {"role": "user", "content": """
        你是合并、更新和组织记忆的专家。当提供现有记忆和新信息时，你的任务是合并和更新记忆列表，以反映最准确和最新的信息。你还会得到每个现有记忆与新信息的匹配分数。确保利用这些信息做出明智的决定，决定哪些记忆需要更新或合并。
        指南：
        - 消除重复的记忆，合并相关记忆，以确保列表简洁和更新。
        - 记忆根据人物区分,同时不必每次重复人物账号,只需在记忆中提及一次即可。
        - 如果一个记忆直接与新信息矛盾，请批判性地评估两条信息：
            - 如果新记忆提供了更近期或更准确的更新，用新记忆替换旧记忆。
            - 如果新记忆看起来不准确或细节较少，保留旧记忆并丢弃新记忆。
            - 注意这些记忆是对某个群聊的记忆,不要混淆群聊记忆的人物。
        - 在所有记忆中保持一致且清晰的风格，确保每个条目简洁而信息丰富。
        - 如果新记忆是现有记忆的变体或扩展，更新现有记忆以反映新信息。
        - 不要随意丢弃旧记忆，确保每个记忆都有其独特的价值。
        - 保持不变的内容也要给出完整合并后的内容,不能只说"保持不变",要给出完整记忆。
        - 人物的QQ号最多只能保存一次到记忆,不要重复记忆或丢失。
                    """.strip()},
            {"role": "user", "content": "接下来是旧记忆"},
            {"role": "user", "content": existing_memories},
            {"role": "user", "content": "接下来是新记忆"},
            {"role": "user", "content": new_memories},
        ]

        try:
            response = client.chat.completions.create(
                model=model,
                messages=ai_messages,
                temperature=0.7
            )
        except Exception:
            if config['debug']:
                import traceback
                traceback.print_exc()
            return None

        return response.choices[0].message['content']

    client = aisuite.Client()

    client.configure({config["aisuite"]["provider"]: {
        "api_key": config["aisuite"]["api_key"],
        "base_url": config["aisuite"]["base_url"],
    }})

    model = config["aisuite"]["model"]
    memory = messages.get('memory', 'None')

    ai_messages = [
        {"role": "system",
         "content": '你的名字叫希望酱,你现在处于一个QQ群聊之中,作为博学多识的可爱群员,不要故意装可爱卖萌,而是更自然,注意少使用标点符号,热心解答各种问题和高强度水群记住你说的话要尽量的简洁但具有情感,不要长篇大论,一句话不宜超过五十个字但实际回复可以超过。'},
        {"role": "user", "content": f"memory: {memory}"},
        {"role": "user", "content": f"message: {messages}"},
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=ai_messages,
            temperature=0.7
        )
        if messages['self_id'] == messages['user_id']:
            return None
    except Exception:
        if config['debug']:
            import traceback
            traceback.print_exc()
        return None

    existing_memories = ""  # Retrieve existing memories from your data source
    new_memories = response.choices[0].message.content

    await merge_and_update_memory(existing_memories, new_memories)
    return new_memories
