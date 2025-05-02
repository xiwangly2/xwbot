import aisuite as ai


async def generate_response(prompt_text):
    """生成 QA响应"""
    from internal.config import config
    client = ai.Client()
    client.configure({config["aisuite"]["provider"]: {
        "api_key": config["aisuite"]["api_key"],
        "base_url": config["aisuite"]["base_url"],
    }})
    _ = client.chat.completions.create(
        model=config["aisuite"]["model"],
        messages=[
            {"role": "system", "content": "你是一个Q群群友，你是人类，我会给你一个json格式的OneBot消息，对于不必要回复的内容，请输出no reply"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
    )
    return _.choices[0].message.content.strip()
