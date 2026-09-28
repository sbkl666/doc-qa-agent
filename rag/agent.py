"""
Agent 核心模块
实现 ReAct 模式的智能体：
1. 工具调用：Agent 自主决定是否需要检索文档
2. 对话记忆：支持多轮对话
3. 引用溯源：回答附带来源文档
"""
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage, AIMessage
from config import config
from rag.vectorstore import vector_store


# ========== 1. 定义 Agent 可用的工具 ==========

@tool
def search_documents(query: str) -> str:
    """
    搜索上传的文档知识库，查找与用户问题相关的内容。
    当用户的问题涉及文档内容时，使用这个工具。
    
    Args:
        query: 要搜索的查询文本
    """
    results = vector_store.similarity_search(query, k=3)
    if not results:
        return "未在文档中找到相关信息。"
    
    # 格式化搜索结果，附带来源
    formatted_results = []
    for i, (doc, score) in enumerate(results):
        source = doc.metadata.get("source", "未知来源")
        page = doc.metadata.get("page", "?")
        chunk_id = doc.metadata.get("chunk_id", "?")
        content = doc.page_content[:300]  # 截取前300字，避免太长
        formatted_results.append(
            f"【来源 {i+1}】文件: {source} | 页码: {page} | 相关度: {score:.4f}\n"
            f"内容摘要: {content}..."
        )
    
    return "\n\n---\n\n".join(formatted_results)


# 工具列表
tools = [search_documents]


# ========== 2. 初始化大模型 ==========

llm_config = config.get_llm_config()
llm = ChatOpenAI(
    model=llm_config["model"],
    api_key=llm_config["api_key"],
    base_url=llm_config["base_url"],
    temperature=config.TEMPERATURE,
)


# ========== 3. 定义 Agent 的 Prompt ==========

SYSTEM_PROMPT = """你是一个专业的文档问答助手。你可以：

1. 使用 search_documents 工具搜索用户上传的文档内容
2. 基于文档内容回答用户的问题
3. 如果问题不需要查文档，直接回答

规则：
- 回答必须基于搜索到的文档内容，不要编造
- 如果文档里找不到答案，明确告诉用户"文档中没有相关信息"
- 回答时引用来源（文件和页码）
- 保持回答简洁清晰

当前已上传文档数量：{doc_count} 个 chunk"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


# ========== 4. 创建 Agent ==========

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 打印 Agent 的思考过程，方便调试
    max_iterations=config.MAX_ITERATIONS,
    early_stopping_method="generate",
)


# ========== 5. 对话管理类 ==========

class DocumentQAAgent:
    """文档问答 Agent 封装"""

    def __init__(self):
        self.chat_history: List = []

    def ask(self, question: str) -> Dict:
        """
        向 Agent 提问
        :param question: 用户问题
        :return: {answer, sources, steps}
        """
        # 获取当前文档数量，更新 prompt 上下文
        doc_count = vector_store.count()
        
        # 调用 Agent
        result = agent_executor.invoke({
            "input": question,
            "chat_history": self.chat_history,
            "doc_count": doc_count,
        })
        
        # 更新对话历史
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=result["output"]))
        
        # 构造返回结果
        return {
            "answer": result["output"],
            "chat_history_length": len(self.chat_history) // 2,
        }

    def reset_history(self):
        """清空对话历史"""
        self.chat_history = []
        print("对话历史已清空")


# 全局实例
doc_agent = DocumentQAAgent()
