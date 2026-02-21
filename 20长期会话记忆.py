import os, json
import pathlib
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory


# message_to_dict: 单个消息对象（BaseMessage类实例） -> 字典
# messages_from_dict: [字典、字典...] -> [消息、消息...]
# AIMessage、HumanMessage、SystemMessage 都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        new_messages = [message_to_dict(message) for message in all_messages]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=4)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


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
# 实现会话id获取InMemoryChatMessageHistory类对象
def get_history(session_id):
    return FileChatMessageHistory(session_id, pathlib.Path("./chat_history"))

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
    res = conversation_chain.invoke({"input":"小明有2只猫"},session_config)
    print("第一次执行:", res)

    res = conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    print("第二次执行:", res)

    res = conversation_chain.invoke({"input": "总共有多少只宠物"}, session_config)
    print("第三次执行:", res)
