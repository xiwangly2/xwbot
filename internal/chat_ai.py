import aisuite as ai


async def chat_ai(messages, message):
    from internal.config import config
    client = ai.Client()

    client.configure({config["aisuite"]["provider"]: {
        "api_key": config["aisuite"]["api_key"],
        "base_url": config["aisuite"]["base_url"],
    }})

    model = config["aisuite"]["model"]

    ai_messages = [
        {"role": "system", "content": "你扮演QQ群里的一只猫娘，我现在把完整的接收消息参数给你，你需要对消息进行回复。"},
        {"role": "user", "content": f"messages: {messages}"},
    ]
    try:
        if messages['self_id'] == messages['user_id']:
            return None
        response = client.chat.completions.create(
            model=model,
            messages=ai_messages,
            temperature=0.75
        )
    except Exception:
        if config['debug']:
            import traceback
            traceback.print_exc()
        return None
    return response.choices[0].message.content
