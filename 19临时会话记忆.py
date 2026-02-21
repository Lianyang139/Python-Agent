import pathlib

from flask import session
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# 本节重点
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()
chat_model = ChatTongyi(model="qwen3-max",api_key=qwApikey)

# prompt = PromptTemplate.from_template(
#     f"你需要根据会话历史回应用户问题。对话历史：{chat_history},用户提示词：{input},请回答"
# )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据会话历史回应用户问题:"),
        MessagesPlaceholder("chat_history"),
        ("human","请回答如下问题:{input}")
    ]
)

str_parser = StrOutputParser()

# 工具函数：用于调试时打印历史会话
def print_prompt(full_prompt):
    print("="*20,full_prompt.to_string(),"="*20)
    return full_prompt

base_chain = prompt | chat_model | str_parser

# 本节重点
# 创建一个空字典，记录每个用户的信息，key = session, value = InMemoryChatMessageHistory类对象
store = {}

# 实现会话id获取InMemoryChatMessageHistory类对象
def get_history(session_id):
    if session_id not in store:    #第一次使用是空的
        store[session_id] = InMemoryChatMessageHistory()    #将session_id的值设置为InMemoryChatMessageHistory()

    return store[session_id]    #返回字典

# 本节重点
# 创建一个新的链，对原有链增强：自动附加历史消息

conversation_chain = RunnableWithMessageHistory(
    base_chain,                     # 增强原有chain
    get_history,                    # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",     # 用户输入在模板中的占位符
    history_messages_key="chat_history",  # 历史
)

if __name__ == "__main__":
    # 固定格式，添加langchain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }

    # ctrl + p 查看函数声明
    res = conversation_chain.invoke({"input":"小明有2只猫"},session_config=session_config)
    print("第一次执行:", res)

    res = conversation_chain.invoke({"input": "小刚有1只狗"}, session_config=session_config)
    print("第二次执行:", res)

    res = conversation_chain.invoke({"input": "总共有多少只宠物"}, session_config=session_config)
    print("第三次执行:", res)