"""
向量数据库模块
负责：文档向量化、存储、相似度搜索
使用 ChromaDB 作为本地向量数据库，不需要额外安装服务
"""
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import config


class VectorStore:
    """向量数据库管理类"""

    def __init__(self):
        self.embeddings = self._init_embeddings()
        self.vectorstore = None
        self._init_vectorstore()

    def _init_embeddings(self) -> OpenAIEmbeddings:
        """初始化 Embedding 模型"""
        embedding_config = config.get_embedding_config()
        return OpenAIEmbeddings(
            model=embedding_config["model"],
            api_key=embedding_config["api_key"],
            base_url=embedding_config["base_url"],
        )

    def _init_vectorstore(self):
        """初始化 ChromaDB 向量库"""
        self.vectorstore = Chroma(
            persist_directory=config.CHROMA_PATH,
            embedding_function=self.embeddings,
        )

    def add_documents(self, documents: List[Document]):
        """
        把文档加入向量库
        :param documents: Document 列表
        """
        if not documents:
            return
        self.vectorstore.add_documents(documents)
        print(f"已添加 {len(documents)} 个 chunk 到向量库")

    def similarity_search(self, query: str, k: int = 3) -> List[Tuple[Document, float]]:
        """
        相似度搜索
        :param query: 查询文本
        :param k: 返回最相似的前 k 个结果
        :return: (Document, 相似度分数) 列表
        """
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return results

    def get_retriever(self, k: int = 3):
        """
        获取 retriever 对象，供 LangChain Chain 使用
        :param k: 返回结果数
        :return: Retriever 对象
        """
        return self.vectorstore.as_retriever(search_kwargs={"k": k})

    def clear(self):
        """清空向量库（删除所有数据）"""
        if self.vectorstore:
            # ChromaDB 没有直接的 clear 方法，我们删掉所有 collection
            collections = self.vectorstore._client.list_collections()
            for col in collections:
                self.vectorstore._client.delete_collection(col.name)
            print("向量库已清空")

    def count(self) -> int:
        """获取向量库中的文档数量"""
        if self.vectorstore:
            return self.vectorstore._collection.count()
        return 0


# 全局实例
vector_store = VectorStore()
