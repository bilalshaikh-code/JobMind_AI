# rag_pipeline.py
from typing import List, Any, Optional
import os
import uuid

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_classic.schema.output_parser import StrOutputParser
from langchain_classic.prompts import PromptTemplate
from langchain_classic.schema.runnable import RunnablePassthrough

import chromadb
import numpy as np


class LoaderManager:
    """Handles loading different document types"""
    
    def __init__(self, file_paths: list[str]):
        self.file_paths = file_paths
        self.documents = []

    def load_documents(self) -> List[Any]:
        """Load all PDFs (you can extend for TXT, DOCX later)"""
        for file_path in self.file_paths:
            try:
                print(f"[DEBUG] Loading: {file_path}")
                loader = PyPDFLoader(str(file_path))
                docs = loader.load()
                self.documents.extend(docs)
                print(f"[INFO] Loaded {len(docs)} pages from {file_path}")
            except Exception as e:
                print(f"[ERROR] Failed to load {file_path}: {e}")
        
        return self.documents


class EmbeddingManager:
    """Handles text splitting and embeddings"""
    
    def __init__(self, 
                 embed_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 chunk_size: int = 800,
                 chunk_overlap: int = 150):
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embed_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        print(f"[INFO] Embedding model loaded: {embed_model}")

    def split_documents(self, documents: List[Any]) -> List[Any]:
        chunks = self.text_splitter.split_documents(documents)
        print(f"[INFO] Split into {len(chunks)} chunks")
        return chunks

    def generate_embeddings(self, chunks: List[Any]) -> np.ndarray:
        texts = [chunk.page_content for chunk in chunks]
        print(f"[INFO] Generating embeddings for {len(texts)} chunks...")
        embeddings = self.embeddings.embed_documents(texts)
        return np.array(embeddings)


class VectorStoreManager:
    """Manages ChromaDB operations"""
    
    def __init__(self, collection_name: str = "jobmind_docs", persist_dir: str = "data/chroma_db"):
        self.collection_name = collection_name
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"[INFO] Vector store initialized: {collection_name}")

    def add_documents(self, chunks: List[Any], embeddings: np.ndarray):
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings count mismatch")

        ids = [f"doc_{uuid.uuid4().hex[:12]}" for _ in chunks]
        metadatas = [dict(chunk.metadata) for chunk in chunks]
        texts = [chunk.page_content for chunk in chunks]
        embeddings_list = embeddings.tolist()

        self.collection.add(
            ids=ids,
            embeddings=embeddings_list,
            metadatas=metadatas,
            documents=texts
        )
        print(f"[SUCCESS] Added {len(chunks)} documents to vector store")


class RAGPipeline:
    """Main RAG Engine"""
    
    def __init__(self):
        self.loader = None
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStoreManager()
        self.llm = ChatOllama(model="llama3.2:1b", temperature=0.3)
        self.retriever = None

    def ingest(self, file_paths: list[str]):
        """Full ingestion pipeline"""
        # 1. Load
        self.loader = LoaderManager(file_paths)
        documents = self.loader.load_documents()

        # 2. Split
        chunks = self.embedding_manager.split_documents(documents)

        # 3. Embed
        embeddings = self.embedding_manager.generate_embeddings(chunks)

        # 4. Store
        self.vector_store.add_documents(chunks, embeddings)
        
        print("Ingestion completed successfully!")

    def query(self, question: str, k: int = 4) -> str:
        """Query the RAG system"""
        if not hasattr(self.vector_store.collection, 'count') or self.vector_store.collection.count() == 0:
            return "Please ingest documents first."

        # Simple retrieval using Chroma (you can improve this)
        results = self.vector_store.collection.query(
            query_texts=[question],
            n_results=k
        )

        context = "\n\n".join(results['documents'][0])

        prompt = PromptTemplate.from_template(
            """You are a helpful career assistant. Use the following context to answer the question.
            
            Context:
            {context}
            
            Question: {question}
            Answer:"""
        )

        chain = (
            prompt 
            | self.llm 
            | StrOutputParser()
        )

        return chain.invoke({"context": context, "question": question})