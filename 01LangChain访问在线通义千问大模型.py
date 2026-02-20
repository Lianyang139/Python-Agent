# langchain_community 社区版
# 实例化模型类对象
# 调用invoke提问，一次性返回完整结果

from langchain_community.llms.tongyi import Tongyi
import pathlib

qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()
print(qwApikey)
qw_model = Tongyi(model="qwen-max", api_key=qwApikey)

#结果一次性输出
res = qw_model.invoke(input="你是谁呀能做什么？")
print(res)
