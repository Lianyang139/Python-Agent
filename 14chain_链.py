# chain链：将上一个组件的输出作为这次的输入
# chain必须是Runnable、Callable、Mapping的子类

import pathlib

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

# 构建提示词
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个诗人，可以作诗"),
        MessagesPlaceholder("history"), #history是字典的key
        ("human","再来一首诗")
    ]
)

# history_data是字典的value
history_data = [
    ("human","你来写一首诗"),
    ("ai","床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human","好诗，再来一首"),
    ("ai","日照香炉生紫烟，遥看瀑布挂前川，不识庐山真面目，只缘身在此山中"),
]

qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()
chat_model = ChatTongyi(model="qwen3-max",api_key=qwApikey)

# 通过chain(链式)注入提示词文本
custom_chain = chat_prompt | chat_model

res = custom_chain.invoke({"history_data":history_data})
print(res.content)

# 使用stream流式输出
for chunk in res.stream({"history_data":history_data}):
    print(chunk.content,end="",flush=True)