"""
提示词：用户的提问 + 向量库中检索到的参考资料
"""
import pathlib

from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()

model = ChatTongyi(model="qwen3-max",api_key=qwApikey)

# 使用参考资料
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("user", "用户提问：{input}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# 准备参考资料（向量库的数据）
# add_texts 传入一个 list[str]
# 注：选择文件资料需要使用文件加载器转换为Document，使用adddocument方法
vector_store.add_texts(["减肥就是要少吃多练", "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"])

# 假设用户提问
input_text = "怎么减肥？"

# 检索向量库（相似度搜索）,这时的类型的Document
result = vector_store.similarity_search(input_text,2)

# 转换为字符串，传入的到context中构建提示词
reference_text = "["
for doc in result:
    reference_text += doc.page_content

reference_text += "]"

print(reference_text)
# 此时reference_text:减肥就是要少吃多练在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来

# 创建chain链
# usage: new *
def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

# chain
chain = prompt | print_prompt | model | StrOutputParser()

# "input"是用户输入，"context"是参考资料
res = chain.invoke({"input": input_text, "context": reference_text})
print(res)