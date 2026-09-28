"""
文档加载与文本切分模块
负责：加载 PDF/TXT 文件，把长文本切成小块（chunk），方便后续向量化
"""
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import config


class DocumentProcessor:
    """文档处理器：加载文件并切分文本"""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", ";", " ", ""],
        )

    def load_pdf(self, file_path: str) -> List[Document]:
        """
        加载 PDF 文件
        :param file_path: PDF 文件路径
        :return: Document 列表，每个 Document 是一页
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents

    def load_txt(self, file_path: str) -> List[Document]:
        """
        加载 TXT 文件
        :param file_path: TXT 文件路径
        :return: Document 列表
        """
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()
        return documents

    def load_file(self, file_path: str) -> List[Document]:
        """
        根据文件后缀自动选择加载方式
        :param file_path: 文件路径
        :return: Document 列表
        """
        if file_path.lower().endswith(".pdf"):
            return self.load_pdf(file_path)
        elif file_path.lower().endswith(".txt") or file_path.lower().endswith(".md"):
            return self.load_txt(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_path}")

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        把长文档切分成小块（chunk）
        :param documents: 原始 Document 列表
        :return: 切分后的 Document 列表
        """
        splits = self.text_splitter.split_documents(documents)
        # 给每个 chunk 加上序号标记，方便溯源
        for i, doc in enumerate(splits):
            doc.metadata["chunk_id"] = i
        return splits

    def process_file(self, file_path: str) -> List[Document]:
        """
        完整流程：加载文件 → 切分文本
        :param file_path: 文件路径
        :return: 处理好的 Document 列表
        """
        documents = self.load_file(file_path)
        splits = self.split_documents(documents)
        print(f"加载 {file_path}: 原始 {len(documents)} 页 → 切分后 {len(splits)} 个 chunk")
        return splits


# 全局实例
doc_processor = DocumentProcessor()
