import streamlit as st
import requests
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Document Q&A System")
st.markdown("Upload documents and ask questions using Retrieval-Augmented Generation")

# Sidebar
with st.sidebar:
    st.header("📄 Document Management")
    
    # Upload document
    uploaded_file = st.file_uploader("Upload Document", type=['pdf', 'txt'])
    if uploaded_file and st.button("Process Document"):
        with st.spinner("Processing document..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{API_URL}/upload", files=files)
            
            if response.status_code == 200:
                st.success(f"✅ Document uploaded: {uploaded_file.name}")
            else:
                st.error(f"❌ Error: {response.text}")
    
    st.divider()
    
    # List documents
    if st.button("🔄 Refresh Documents"):
        st.rerun()
    
    try:
        response = requests.get(f"{API_URL}/documents")
        if response.status_code == 200:
            docs = response.json()["documents"]
            st.subheader(f"Documents ({len(docs)})")
            
            for doc in docs:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(doc['source'].split('/')[-1])
                with col2:
                    if st.button("🗑️", key=doc['doc_id']):
                        requests.delete(f"{API_URL}/documents/{doc['doc_id']}")
                        st.rerun()
    except:
        st.warning("⚠️ Cannot connect to API")

# Main area - Q&A
st.header("💬 Ask Questions")

question = st.text_input("Enter your question:", placeholder="What is this document about?")

col1, col2 = st.columns([1, 4])
with col1:
    top_k = st.number_input("Top K Results", min_value=1, max_value=10, value=3)

if st.button("🔍 Search", type="primary"):
    if not question:
        st.warning("Please enter a question")
    else:
        with st.spinner("Searching documents..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": question, "top_k": top_k}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.subheader("📝 Answer")
                    st.write(result["answer"])
                    
                    st.divider()
                    
                    st.subheader("📚 Sources")
                    for i, source in enumerate(result["sources"], 1):
                        st.text(f"{i}. {source.split('/')[-1]}")
                else:
                    st.error(f"Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Cannot connect to API: {e}")

# Footer
st.divider()
st.markdown("""
### 🚀 Features
- **Upload Documents**: PDF and TXT files supported
- **Semantic Search**: ChromaDB vector store with Ollama embeddings
- **RAG Architecture**: LangChain-powered retrieval and generation
- **Production Ready**: FastAPI backend with Docker deployment
""")
