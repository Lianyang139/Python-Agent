import pathlib

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

# 解析器，将AI的回答作为问题给AI让其继续回答
parser = StrOutputParser()

qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()
chat_model = ChatTongyi(model="qwen3-max",api_key=qwApikey)

prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},你帮我起个名字，简单回答。"
)

# 解析器parser什么都不用做，加入链即可
chain = prompt | chat_model | parser | chat_model

res:AIMessage = chain.invoke({"lastname":"张","gender":"女儿"}) # 此处的AIMessage为类型注解
print(res.content)

"""
chain = prompt | chat_model | parser | chat_model | parser
res:str = chain.invoke({"lastname":"张","gender":"女儿"})
print(res)
再添加了一个parser解析器后，原res的类型就由AIMessage转变成了str

chain = prompt | chat_model | parser | chat_model的做法并不是真正的工作流
正确的方法应该是：
invoke | stream 初始输入-提示词-模型-数据处理-新提示词模版-模型-解析器-结果

将模型的AIMessage-转化为字典-注入第二个提示词模版中，形成新的提示词（promptvalue对象）
"""
