# Example: reuse your existing OpenAI setup
from openai import OpenAI
def breeze(prompt):
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
    model="Breeze FT/breeze ft",
    messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "你好"}
    ],
    temperature=0.7,
    )
    # 给定字符串
    string = str(completion.choices[0].message)
    # 使用 split() 函数分割字符串
    content_start = string.find("content=")
    content_end = string.find(", role=")
    content = string[content_start + len("content=\""):content_end - 1]
    # 打印提取的内容
    return content
