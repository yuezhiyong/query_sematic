# -*- coding: utf-8 -*-
import streamlit as st
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

st.title("个人语义搜索引擎")

# 加载相同的嵌入模型
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

# 连接已存在的数据库
db = Chroma(
            persist_directory="./chroma_db",
                embedding_function=embedding_model
                )

# 搜索框
query = st.text_input("输入你想搜索的内容：")
if query:
# 执行相似度搜索
    results = db.similarity_search_with_score(query, k=5)
                                      
    st.subheader("搜索结果：")
    for doc, score in results:
    # 过滤低分结果
        if score < 0.5: 
            continue
        st.markdown(f"**相关度得分**: {1 - score:.4f}") # Chroma 返回的是距离，越小越相似
        st.markdown(f"**来源**: {doc.metadata.get('source', 'Unknown')}")
        st.markdown(f"**内容**: {doc.page_content[:200]}...")
        st.divider()
