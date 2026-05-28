import os
from openai import OpenAI
import gradio as gr

messages=[{"role": "system", "content": "這是一個基於四柱八字的聊天機器人，旨在提供洞察力強的讀數與事實信息相結合。"},]

def myAssist2(prompt, history):
  history = history or []
  global messages

  messages.append({'role':'user', 'content':prompt})
  client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
  response = client.chat.completions.create(
      model=os.getenv("OPENAI_FINETUNED_MODEL", "gpt-3.5-turbo"),
      messages = messages
  )
  reply = response.choices[0].message.content
  messages.append({'role':'assistant', 'content':reply})
  history = history + [[prompt, reply]]
  return reply
demo = gr.ChatInterface(myAssist2)
demo.launch(share=True)
