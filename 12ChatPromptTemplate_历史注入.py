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

# 通过invoke注入提示词文本
prompt_text = chat_prompt.invoke({"history":history_data}).to_string()
print(prompt_text)

qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()
chat_model = ChatTongyi(model="qwen3-max",api_key=qwApikey)
res = chat_prompt.invoke(prompt_text)
print(res.content)
