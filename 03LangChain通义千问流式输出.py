# langchain_community 社区版
# 实例化模型类对象
# stream返回结果流式输出

from langchain_community.llms.tongyi import Tongyi
import pathlib

qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()
print(qwApikey)
qw_model = Tongyi(model="qwen-max", api_key=qwApikey)

#结果流式输出,打印需要for循环方法,每次flush刷新
res = qw_model.stream(input="你是谁呀能做什么？")
for chunk in res:
    print(chunk,end="",flush=True)
