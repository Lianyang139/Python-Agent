# 字符串转向量，语义判断
# Ollama官网：https://ollama.com/search
# 首页进入Models/Embedding/qwen3-embedding/(命令行下载)
# 本地客户端中下载

from langchain_ollama.embeddings import OllamaEmbeddings

# 创建模型类对象，默认text-embeddings-v1
ollamaEmbed_Model = OllamaEmbeddings(model="qwen3-embedding:4b")

# embed_query 单次转换,embed_documents 多次转换
embedding = ollamaEmbed_Model.embed_query("我喜欢你")
print(f"嵌入向量长度: {len(embedding)}")
print(f"前5个值: {embedding[:5]}")  # 打印前5个维度看看

embed_documents = ollamaEmbed_Model.embed_documents(["我喜欢你","我稀饭你","晚上吃啥"])
print(f"共生成 {len(embed_documents)} 个向量")
for i, vec in enumerate(embed_documents):
    print(f"第 {i+1} 个句子的向量维度: {len(vec)}")
    print(f"前5个值: {[round(x, 4) for x in vec[:5]]}")
    print("-" * 40)
