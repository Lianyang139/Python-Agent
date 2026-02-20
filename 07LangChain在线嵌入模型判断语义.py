# 字符串转向量，语义判断
import pathlib
from langchain_community.embeddings import DashScopeEmbeddings

myApiKey = pathlib.Path("key.txt").read_text(encoding="utf-8-sig").strip()
# 创建模型类对象，默认text-embeddings-v1
dashscope_Model = DashScopeEmbeddings(dashscope_api_key=myApiKey)

# embed_query 单次转换,embed_documents 多次转换
embedding = dashscope_Model.embed_query("我喜欢你")
print(f"嵌入向量长度: {len(embedding)}")
print(f"前5个值: {embedding[:5]}")  # 打印前5个维度看看

embed_documents = dashscope_Model.embed_documents(["我喜欢你","我稀饭你","晚上吃啥"])
print(f"共生成 {len(embed_documents)} 个向量")
for i, vec in enumerate(embed_documents):
    print(f"第 {i+1} 个句子的向量维度: {len(vec)}")
    print(f"前5个值: {[round(x, 4) for x in vec[:5]]}")
    print("-" * 40)
