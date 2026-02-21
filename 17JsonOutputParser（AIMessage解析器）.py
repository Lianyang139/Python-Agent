import pathlib

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

# 解析器，将AI的回答作为问题给AI让其继续回答
str_parser = StrOutputParser()
json_parser = JsonOutputParser()

qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()
chat_model = ChatTongyi(model="qwen3-max",api_key=qwApikey)

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},请起名字,"
    "并封装为JSON格式返回给我。要求kye是name,value是你起的名字，请严格遵守要求"
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name},请帮我解析含义"
)

# 解析器parser什么都不用做，加入链即可
chain = first_prompt | chat_model | json_parser | chat_model | str_parser

for chunk in chain.stream({"lastname":"张","gender":"女儿"}):
    print(chunk,end="",flush=True)

"""
invoke | stream 初始输入-提示词-模型-数据处理-新提示词模版-模型-解析器-结果
将模型的AIMessage-转化为字典-注入第二个提示词模版中，形成新的提示词（promptvalue对象）
"""
