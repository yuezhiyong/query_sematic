import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. 配置嵌入模型 (使用对中文友好的 BGE-M3)
# 首次运行会自动下载模型，约 1-2GB，注意磁盘空间
embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
                model_kwargs={'device': 'cpu'}, # 如果有 GPU 可改为 'cuda'
                    encode_kwargs={'normalize_embeddings': True}
                    )

# 2. 加载数据 (假设你的笔记在 ./data 目录)
loader = DirectoryLoader("./data", glob="**/*.md", loader_cls=TextLoader)
documents = loader.load()

# 3. 文本切片 (避免片段太长或太短)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# 4. 存入向量数据库 (持久化到本地磁盘)
db = Chroma.from_documents(
            documents=chunks,
                embedding=embedding_model,
                    persist_directory="./chroma_db" # 重要：数据持久化
                    )

print(f"索引完成，共存入 {len(chunks)} 个片段")
