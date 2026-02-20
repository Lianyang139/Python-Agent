# Prompet
from langchain_core.prompts import PromptTemplate
# 可以使用llm模型，也可以使用chat_model
from langchain_community.llms.tongyi import Tongyi
import pathlib

myApi_key = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()

# 创建模型类对象
ty_model = Tongyi(model="qwen-max",api_key=myApi_key)

# 提示词模版
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},你帮我起个名字，简单回答。"
)

# 标准写法
# 使用.format方法注入信息,目的是为了得到prompt_template类型的对象
# prompt_text = prompt_template.format(lastname = "张",gender = "女儿" )
# print(prompt_text)

# res = ty_model.invoke(input=prompt_text)
# print(res)


# 链式写法(现有提示词prompt_template，然后放到ty_model中去使用)
# zero-shot(依赖于模型内部训练回答)
chain = prompt_template | ty_model
# 通chain调用invoke，需要使用字典形式
res = chain.invoke(input={"lastname":"张","gender":"女儿"})
print(res)