# Fewshot Prompt 提示词
import pathlib
from sys import prefix

from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from scripts.regsetup import examples

myApi_key = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()

# 示例的模版
Prompt_Template = PromptTemplate.from_template("单词:{word},反义词:{antonym}")
# 示例的动态数据注入,使用list字典格式,等价于现教大模型没有训练到的知识
examples_data = [
    {"word":"大","antonym":"小"},
    {"word":"上","antonym":"下"}
]

# 需要5个参数，(示例数据模版)(示例数据)(示例之前的提示词)(示例之后的提示词)(注入的变量名)
# FewShotPromptTemplate(
#     example_prompt=None,    # 示例数据模版
#     examples=None,          # 示例数据(注入动态数据，需要使用list格式)
#     prefix=None,            # 示例之前的提示词
#     suffix=None,            # 示例之后的提示词
#     input_variables=[]      # 声明在前缀或后缀中所需要注入的变量名
# )

few_shot_template = FewShotPromptTemplate(
    example_prompt=Prompt_Template,             # 示例数据模版
    examples=examples_data,                     # 示例数据(注入动态数据，需要使用list格式)
    prefix="告知我单词的反义词，我提供如下示例：",           # 我告诉AI的
    suffix="基于前面的示例告诉我{input_word}的反义词是？",  # 我要求AI做的
    input_variables=["input_word"]      # 声明在前缀或后缀中所需要注入的变量名
)

# 动态提示词文本
prompt_text = few_shot_template.invoke(input={"input_word":"左"}).to_string()
print(prompt_text)

# 调用模型
from langchain_community.llms.tongyi import Tongyi

Tongyi_model = Tongyi(model="qwen-max",api_key=myApi_key)
Tongyi_model.invoke(input=prompt_text)