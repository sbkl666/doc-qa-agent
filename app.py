"""
Streamlit Web 界面
主入口文件，运行: streamlit run app.py
"""
import streamlit as st
import os
import tempfile
from rag.loader import doc_processor
from rag.vectorstore import vector_store
from rag.agent import doc_agent


# ========== 页面配置 ==========
st.set_page_config(
    page_title="文档问答 Agent",
    page_icon="📚",
    layout="wide",
)

st.title("📚 文档问答智能体")
st.caption("基于 ReAct Agent + RAG 的文档问答系统")


# ========== 侧边栏：文档管理 ==========
with st.sidebar:
    st.header("📁 文档管理")
    
    # 上传文件
    uploaded_file = st.file_uploader(
        "上传文档（PDF / TXT / Markdown）",
        type=["pdf", "txt", "md"],
    )
    
    if uploaded_file and st.button("📥 上传并索引", type="primary"):
        with st.spinner("正在处理文档..."):
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}"
            ) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            try:
                # 处理文档
                documents = doc_processor.process_file(tmp_path)
                # 加入向量库
                vector_store.add_documents(documents)
                st.success(f"✅ 文档「{uploaded_file.name}」已成功索引！")
            except Exception as e:
                st.error(f"❌ 处理失败: {str(e)}")
            finally:
                # 删除临时文件
                os.unlink(tmp_path)
    
    st.divider()
    
    # 显示当前文档数量
    doc_count = vector_store.count()
    st.metric("📊 已索引文档块数", doc_count)
    
    # 清空对话按钮
    if st.button("🗑️ 清空对话历史"):
        doc_agent.reset_history()
        st.session_state.messages = []
        st.success("对话已清空")
    
    st.divider()
    st.caption("💡 提示：先上传文档，然后在右侧提问")


# ========== 主界面：聊天窗口 ==========

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入你的问题..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 调用 Agent
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                result = doc_agent.ask(prompt)
                answer = result["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"❌ 出错了: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
