# 📚 文档问答智能体

基于 **ReAct Agent + RAG** 的文档问答系统，支持上传 PDF/TXT 文档并进行智能问答。

## ✨ 功能特性

- 📄 **多格式支持**：支持 PDF、TXT、Markdown 文档上传
- 🤖 **Agent 驱动**：基于 ReAct 范式，Agent 自主判断是否需要检索文档
- 🔍 **RAG 检索**：向量相似度搜索，快速定位相关内容
- 💬 **多轮对话**：支持上下文记忆，连续追问
- 🎨 **Web 界面**：基于 Streamlit 的交互式界面

## 🏗️ 项目架构

```
doc-qa-agent/
├── app.py              # Streamlit 主入口
├── config.py           # 配置管理
├── requirements.txt    # 依赖清单
├── .env.example        # 环境变量模板
└── rag/                # RAG 核心模块
    ├── loader.py       # 文档加载与切分
    ├── vectorstore.py  # 向量数据库
    └── agent.py        # Agent 核心逻辑
```

## 🚀 快速开始

### 1. 环境要求
- Python 3.9+
- 大模型 API Key（豆包 / 通义千问）

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

### 4. 运行应用
```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| Agent 框架 | LangChain |
| 大模型 | 豆包 / 通义千问（OpenAI 兼容接口） |
| 向量数据库 | ChromaDB |
| Web 框架 | Streamlit |
| 文本切分 | RecursiveCharacterTextSplitter |

## 📝 使用说明

1. **上传文档**：在左侧边栏上传 PDF/TXT 文件
2. **等待索引**：系统自动将文档切分、向量化并存入向量库
3. **开始提问**：在右侧聊天窗口输入问题，Agent 会自动判断是否需要检索文档
4. **多轮对话**：支持连续追问，系统会记住上下文

## 🎯 核心技术点

### ReAct Agent 循环
Agent 按照 **思考 → 行动 → 观察 → 回答** 的循环工作：
1. 用户提问后，Agent 先思考是否需要查文档
2. 如果需要，调用 `search_documents` 工具检索相关内容
3. 基于检索结果生成回答
4. 如果不需要查文档，直接回答

### RAG 流程
```
文档加载 → 文本切分 → 向量化 → 向量存储 → 相似度检索 → 拼接上下文 → LLM 生成答案
```

## 📄 License

MIT
