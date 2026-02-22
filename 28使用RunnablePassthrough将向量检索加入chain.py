"""
提示词：用户的提问 + 向量库中检索到的参考资料
"""
import pathlib

from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
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

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4",dashscope_api_key=qwApikey ))

# 准备参考资料（向量库的数据）
# add_texts 传入一个 list[str]
# 注：选择文件资料需要使用文件加载器转换为Document，使用adddocument方法
vector_store.add_texts(["减肥就是要少吃多练", "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"])

# 假设用户提问
input_text = "怎么减肥？"

# 需求：把向量检索加入chain链
# 因为InMemoryVectorStore无法直接加入chain
# langchain中的方法 as_retriever 可以返回一个Runnable接口的子类实例对象

# serch_kwargs中的参数：
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

"""
# chain
chain = retriever | prompt | model | StrOutputParser()

retriever:
  - 输入: 用户的提问             str
  - 输出: 向量库的检索结果        list[Document] ：问题是Document中没有用户提问，导致信息丢失

prompt:
  - 输入: 用户的提问 + 向量库的检索结果     dict
  - 输出: 完整的提示词                  PromptValue
"""

# 实际应该是
# 基础：“()” 的含义： RunnablePassthrough为类本身，RunnablePassthrough()为类对象
# 解释：使用chain.invoke(...)时
# 通过RunnablePassthrough()对象将用户的输入"input"复制了一份，原始的给“context”，复制的给“input”
# 从而保留了用户的输入，即：用户的提问
# format_func是占位符,目的是将retriever返回的list[Document]转换为字符串后注入给"context"

def format_func(docs):
    if not docs:
        return "无相关参考资料"

    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content

    formatted_str += "]"
    return formatted_str

# 此时的"context": retriever | format_func的含义是：retriever 或 format_func函数返回的结果
chain = ({"input":RunnablePassthrough(),"context": retriever | format_func }| prompt | model | StrOutputParser())

# chain.invoke(...)中的内容是直接提供给"context": retriever
# 所以这样里需要的是str
res = chain.invoke(input_text)
print(res)