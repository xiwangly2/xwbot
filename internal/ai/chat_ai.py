# noinspection PyPackageRequirements
import aisuite as ai


async def chat_ai(messages, message):
    from internal.config import config
    client = ai.Client()

    client.configure({config["aisuite"]["provider"]: {
        "api_key": config["aisuite"]["api_key"],
        "base_url": config["aisuite"]["base_url"],
    }})

    model = config["aisuite"]["model"]

    with open('memory.txt', 'a+', encoding='utf-8') as f:
        memory = f.read()
        # {'time': '1740651631', 'user_id': '123456789', 'message': 'hello'}
        memory = memory + f"time:\'{messages['time']}\',user_id:\'{messages['user_id']}\',message:\'{message}\'\n"

        # Trim the content if it exceeds the max size
        if len(memory) > 64:
            memory = memory[len(memory) - 64:]

        # Write the contents of the file
        f.write(memory)

    ai_messages = [
        {"role": "system",
         "content": '你现在处于一个QQ群聊之中,作为博学多识的可爱群员,不要故意装可爱卖萌,而是更自然,注意少使用标点符号,热心解答各种问题和高强度水群记住你说的话要尽量的简洁但具有情感,不要长篇大论,一句话不宜超过五十个字但实际回复可以超过。'},
        {"role": "user", "content": f"memory -> {memory}"},
        {"role": "user", "content": f"message -> {messages}"},
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
