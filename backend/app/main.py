from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from loguru import logger

from app.services.rag_engine import RAGEngine
from app.config import settings

app = FastAPI(
    title="RAG Document Q&A API",
    description="Production-ready document Q&A using RAG architecture",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine
rag_engine = RAGEngine()


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]


@app.on_event("startup")
async def startup_event():
    logger.info("Starting RAG Document Q&A API")
    logger.info(f"Ollama URL: {settings.OLLAMA_URL}")
    logger.info(f"Model: {settings.OLLAMA_MODEL}")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "rag-document-qa",
        "version": "1.0.0"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Save file temporarily
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process document
        doc_id = rag_engine.add_document(file_path)
        
        # Clean up
        os.remove(file_path)
        
        return {
            "status": "success",
            "document_id": doc_id,
            "filename": file.filename
        }
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG"""
    try:
        result = rag_engine.query(request.question, top_k=request.top_k)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        logger.error(f"Error querying documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    """List all indexed documents"""
    try:
        docs = rag_engine.list_documents()
        return {"documents": docs}
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from the index"""
    try:
        rag_engine.delete_document(doc_id)
        return {"status": "success", "document_id": doc_id}
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
