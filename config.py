"""
配置管理模块
从 .env 文件读取所有配置
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    """项目配置"""

    # 模型提供商
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "doubao")

    # 豆包配置
    DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY", "")
    DOUBAO_BASE_URL = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    DOUBAO_MODEL = os.getenv("DOUBAO_MODEL", "doubao-pro-32k")

    # 通义千问配置
    QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
    QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

    # Embedding 配置
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "")
    EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "")

    # 向量数据库路径
    CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")

    # 文本切分参数
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

    # Agent 参数
    MAX_ITERATIONS = 5
    TEMPERATURE = 0.1

    @classmethod
    def get_llm_config(cls):
        """根据当前选择的提供商返回 LLM 配置"""
        if cls.MODEL_PROVIDER == "doubao":
            return {
                "api_key": cls.DOUBAO_API_KEY,
                "base_url": cls.DOUBAO_BASE_URL,
                "model": cls.DOUBAO_MODEL,
            }
        elif cls.MODEL_PROVIDER == "qwen":
            return {
                "api_key": cls.QWEN_API_KEY,
                "base_url": cls.QWEN_BASE_URL,
                "model": cls.QWEN_MODEL,
            }
        else:
            raise ValueError(f"不支持的模型提供商: {cls.MODEL_PROVIDER}")

    @classmethod
    def get_embedding_config(cls):
        """返回 Embedding 配置"""
        return {
            "api_key": cls.EMBEDDING_API_KEY or cls.get_llm_config()["api_key"],
            "base_url": cls.EMBEDDING_BASE_URL or cls.get_llm_config()["base_url"],
            "model": cls.EMBEDDING_MODEL,
        }


# 全局配置实例
config = Config()
