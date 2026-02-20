# 静态消息
from langchain_community.chat_models.tongyi import ChatTongyi
import pathlib

myApiKey = pathlib.Path("key.txt").read_text(encoding="utf-8-sig").strip()
chat_model = ChatTongyi(model="qwen3-max",api_key = myApiKey)

# 使用二元元组的消息格式
messages = [
    #给AI设定角色
    ("system","你是一个大名鼎鼎的诗人"),
    ("human","写一首诗"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human","按照你上一个回复的格式，再写一首诗。")
]

res = chat_model.stream(input=messages)

# 聊天模型需要通过.content获取内容
for chunk in res:
    print(chunk.content,end="",flush=True)