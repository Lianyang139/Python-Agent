import pathlib

from chromadb.segment.impl.vector.hnsw_params import persistent_param_validators
from langchain_chroma import Chroma

# DashScopeEmbeddings是千问提供的向量存储
from langchain_community.embeddings import DashScopeEmbeddings
from openai import vector_stores
from langchain_community.document_loaders import CSVLoader

# Chroma 向量数据库
# 安装 langchain-chroma ,chromadb
# 安装方法 pip install


qwApikey = pathlib.Path("key.txt").read_text(encoding='utf-8-sig').strip()

#chat_model = ChatTongyi(model="qwen3-max",api_key=qwApikey)

# 本节重点
# InMemoryVectorStore内存存储
# 向量存储对象用于数据的增、删、改、查
vector_store = Chroma(
    # 数据库的表名称
    collection_name="test",

    #嵌入模型
    embedding_function=DashScopeEmbeddings(dashscope_api_key=qwApikey),

    # 指定数据存放的文件夹,没有会自动创建,生成一个chroma.sqlite3
    persist_directory="./chroma_db"
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",         #指定数据来源
)

documents =loader.load()

# id1 id2 id3 id4 ...
# 向量存储的：新增、删除、检索
vector_store.add_documents(
    documents = documents,      # 被添加的文档，类型：list[Document]

    # 给添加的文档设置id(字符串),list[str]
    # 文档中只有10条数据，source,info不是数据，所以循环要+1
    ids = ["id" + str(i) for i in range(1,len(documents)+1)]
)

# 删除 传入id执行删除
vector_store.delete(["id1","id2"])

# 检索 字符串 返回类型 list[Document]
result = vector_store.similarity_search(

   # 需要检索内容
   "Python是不是简单易学呀",

    #检索的结果要几个
    3 ,

    # 过滤
    filter={"source":"黑马程序员"}
)
print(result)