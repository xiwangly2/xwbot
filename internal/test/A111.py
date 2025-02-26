import os

import aisuite as ai
client = ai.Client()

client.configure({"openai": {
  "api_key": os.environ["ANTHROPIC_API_KEY"],
  "base_url": "https://vip.bili2233.work/v1",
}})

model = "openai:gemini-2.0-flash"

messages = [
    {"role": "system", "content": "只需要回复要求的文本内容。"},
    {"role": "user", "content": "生成通用的实习的今日总结，一两句文字即可。"},
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.75
)

print(response.choices[0].message.content)
