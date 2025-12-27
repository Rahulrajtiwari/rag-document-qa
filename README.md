# 📚 RAG Document Q&A System

Production-ready document Q&A system using **Retrieval-Augmented Generation (RAG)** architecture with **LangChain**, **ChromaDB**, and **Ollama**.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1-orange.svg)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 🚀 Features

- **📄 Document Upload**: Support for PDF and TXT files
- **🔍 Semantic Search**: ChromaDB vector store with Ollama embeddings
- **🤖 RAG Architecture**: LangChain-powered retrieval and generation
- **⚡ FastAPI Backend**: High-performance REST API
- **🎨 Streamlit Frontend**: Beautiful, interactive UI
- **🐳 Docker Ready**: Complete containerized deployment
- **📊 Production Ready**: Proper error handling, logging, and monitoring

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Streamlit  │─────▶│   FastAPI    │─────▶│   Ollama    │
│  Frontend   │      │   Backend    │      │    LLM      │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   ChromaDB   │
                     │ Vector Store │
                     └──────────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, LangChain, Python 3.11
- **Vector Store**: ChromaDB
- **LLM**: Ollama (tinyllama)
- **Frontend**: Streamlit
- **Deployment**: Docker, Docker Compose

## 📦 Quick Start

### Prerequisites

- Docker & Docker Compose
- 4GB+ RAM
- 10GB+ disk space

### Run with Docker

```bash
# Clone the repository
git clone https://github.com/Rahulrajtiwari/rag-document-qa.git
cd rag-document-qa

# Start all services
docker-compose up -d

# Pull the Ollama model
docker exec -it rag-ollama ollama pull tinyllama

# Access the application
# Frontend: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

## 📖 Usage

### 1. Upload Documents

- Open the Streamlit UI at `http://localhost:8501`
- Upload PDF or TXT files using the sidebar
- Documents are automatically processed and indexed

### 2. Ask Questions

- Enter your question in the main text input
- Adjust the "Top K Results" to control context size
- Click "Search" to get AI-powered answers with sources

### 3. API Integration

```python
import requests

# Upload document
files = {"file": open("document.pdf", "rb")}
response = requests.post("http://localhost:8000/upload", files=files)

# Query documents
query = {"question": "What is this document about?", "top_k": 3}
response = requests.post("http://localhost:8000/query", json=query)
print(response.json())
```

## 🔧 Configuration

Environment variables in `docker-compose.yml`:

```yaml
OLLAMA_URL: http://ollama:11434
OLLAMA_MODEL: tinyllama
CHROMA_PERSIST_DIR: /app/data/chroma
CHUNK_SIZE: 1000
CHUNK_OVERLAP: 200
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/upload` | POST | Upload document |
| `/query` | POST | Query documents |
| `/documents` | GET | List documents |
| `/documents/{id}` | DELETE | Delete document |

## 🎯 Use Cases

- **Knowledge Base**: Build searchable documentation systems
- **Research Assistant**: Query research papers and articles
- **Legal/Compliance**: Search through contracts and policies
- **Customer Support**: Answer questions from product manuals
- **Education**: Interactive learning from textbooks

## 🔐 Production Considerations

- Add authentication/authorization
- Implement rate limiting
- Use production-grade vector store (e.g., Pinecone, Weaviate)
- Deploy on Kubernetes for scalability
- Add monitoring and observability
- Implement document versioning

## 📝 Project Structure

```
rag-document-qa/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   └── services/
│   │       └── rag_engine.py    # RAG implementation
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Streamlit UI
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Rahul Kumar Tiwari**

- GitHub: [@Rahulrajtiwari](https://github.com/Rahulrajtiwari)
- LinkedIn: [Rahul Kumar Tiwari](https://www.linkedin.com/in/rahul-tiwari-devops)

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the RAG framework
- [ChromaDB](https://www.trychroma.com/) for the vector store
- [Ollama](https://ollama.ai/) for local LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework

---

⭐ If you find this project useful, please consider giving it a star!
