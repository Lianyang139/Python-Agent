from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate

"""
PromptTemplate->StringPromptTemplate->BasePromptTemplate->Runnable
FewShotPromptTemplate->StringPromptTemplate->BasePromptTemplate->Runnable
ChatPromptTemplate->BaseChatPromptTemplate->BasePromptTemplate->Runnable

所有Runnable的子类都可以使用‘|’链接成为链条

template.format只能接入一条消息，单次对话
from_messages可以从列表中获取多轮对话作为聊天的基础模板(临时记忆)
"""
template = PromptTemplate.from_template("我的邻居是：{lastname},最喜欢：{hobby}")

# 返回字符串
res = template.format(lastname="张大明",hobby="钓鱼")
print(res,type(res)) #打印类型是字符串<class 'str'>

# 返回langchain_core.prompt_values.StringPromptValue的类对象
res2 = template.invoke({"lastname":"周杰伦","hobby":"唱歌"})
print(res2,type(res2)) # 打印类型是<class langchain_core.prompt_values.StringPromptValue>

