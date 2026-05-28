import os
from openai import OpenAI


def GPT_response(text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_FINETUNED_MODEL", "gpt-3.5-turbo"),
        messages=[
            {"role": "system", "content": "這是一個基於四柱八字的聊天機器人，旨在提供洞察力強的讀數與事實信息相結合。"},
            {"role": "user", "content": text}
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].message.content
    return answer

# 調用微調模型生成回答


#-----------------------------------------------------------------------------------------------------------

def GPT3_5_response(text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個命理諮詢師，用引導的方式，我會給你一個對話，幫我把回答的內容豐富點、更有趣，你要扮演回答的位置，將原本的A不改語意方式改寫，用你的對話來取代A，不要重複Q以及直接回答不要有A"},
             {"role": "user", "content": text}
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].message.content
    return answer
 


def GPT_response4o(text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一個命理諮詢師，用引導的方式，我會給你一個對話，幫我把回答的內容豐富點、更有趣，你要扮演回答的位置，將原本的A不改語意方式改寫，用你的對話來取代A，不要重複Q以及直接回答不要有A"},
            {"role": "user", "content": text}
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].message.content
    return answer