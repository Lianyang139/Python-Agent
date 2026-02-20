from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
import pathlib

myApiKey = pathlib.Path("key.txt").read_text(encoding="utf-8-sig").strip()
chat_model = ChatOllama(model="qwen3:4b",api_key = myApiKey)

# fewshot的少量示例方法
messages = [
    #给AI设定角色
    SystemMessage(content="你是一个大名鼎鼎的诗人"),
    HumanMessage(content="写一首诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一个回复的格式，再写一首诗。")
]

res = chat_model.stream(input=messages)

# 聊天模型需要通过.content获取内容
for chunk in res:
    print(chunk.content,end="",flush=True)