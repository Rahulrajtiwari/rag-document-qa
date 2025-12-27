from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from typing import List, Dict
import uuid
from loguru import logger

from app.config import settings


class RAGEngine:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            base_url=settings.OLLAMA_URL,
            model=settings.OLLAMA_MODEL
        )
        
        self.vectorstore = Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            embedding_function=self.embeddings
        )
        
        self.llm = Ollama(
            base_url=settings.OLLAMA_URL,
            model=settings.OLLAMA_MODEL
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        logger.info("RAG Engine initialized")
    
    def add_document(self, file_path: str) -> str:
        """Add a document to the vector store"""
        try:
            # Load document based on file type
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path)
            
            documents = loader.load()
            
            # Split documents
            splits = self.text_splitter.split_documents(documents)
            
            # Generate document ID
            doc_id = str(uuid.uuid4())
            
            # Add metadata
            for split in splits:
                split.metadata['doc_id'] = doc_id
                split.metadata['source'] = file_path
            
            # Add to vectorstore
            self.vectorstore.add_documents(splits)
            self.vectorstore.persist()
            
            logger.info(f"Added document {doc_id} with {len(splits)} chunks")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise
    
    def query(self, question: str, top_k: int = 3) -> Dict:
        """Query the document store"""
        try:
            # Create retrieval chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": top_k}
                ),
                return_source_documents=True
            )
            
            # Run query
            result = qa_chain({"query": question})
            
            # Extract sources
            sources = [
                doc.metadata.get('source', 'Unknown')
                for doc in result['source_documents']
            ]
            
            return {
                "answer": result['result'],
                "sources": list(set(sources))
            }
            
        except Exception as e:
            logger.error(f"Error querying: {e}")
            raise
    
    def list_documents(self) -> List[Dict]:
        """List all indexed documents"""
        try:
            # Get all documents from vectorstore
            collection = self.vectorstore._collection
            results = collection.get()
            
            # Extract unique document IDs
            doc_ids = set()
            docs = []
            
            for metadata in results['metadatas']:
                doc_id = metadata.get('doc_id')
                if doc_id and doc_id not in doc_ids:
                    doc_ids.add(doc_id)
                    docs.append({
                        'doc_id': doc_id,
                        'source': metadata.get('source', 'Unknown')
                    })
            
            return docs
            
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            raise
    
    def delete_document(self, doc_id: str):
        """Delete a document from the vector store"""
        try:
            # Get collection
            collection = self.vectorstore._collection
            
            # Delete all chunks with this doc_id
            collection.delete(where={"doc_id": doc_id})
            
            logger.info(f"Deleted document {doc_id}")
            
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise
