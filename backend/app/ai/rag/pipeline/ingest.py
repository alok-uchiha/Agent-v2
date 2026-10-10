from uuid import uuid4

from langchain_core.documents import Document

from backend.app.ai.rag.splitters.text_splitter_file import split_documents
from backend.app.ai.rag.embeddings.openrouter_embedding import OpenRouterEmbeddings
from backend.app.ai.rag.vectorstores.qdrant_store import QdrantStore

EMBEDDING_MODEL= "nvidia/nemotron-3-embed-1b:free"

def ingest_documents(
        documents:list[Document],
        embedding_model:OpenRouterEmbeddings,
        vector_store:QdrantStore,
)-> None:

    chunks = split_documents(documents)

    if not chunks:
        return

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    vector = embedding_model.embed_documents(texts)

    ids =[
        str(uuid4())
        for _ in chunks
    ]

    vector_store.upsert_documents(
        documents=chunks,
        vectors=vector,
        ids=ids
    )

