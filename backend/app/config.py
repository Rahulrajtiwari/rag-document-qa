from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Ollama Settings
    OLLAMA_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "tinyllama"
    
    # ChromaDB Settings
    CHROMA_PERSIST_DIR: str = "/app/data/chroma"
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    class Config:
        env_file = ".env"


settings = Settings()
