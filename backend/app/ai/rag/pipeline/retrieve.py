from langchain_core.documents import Document

from backend.app.ai.rag.embeddings.openrouter_embedding import OpenRouterEmbeddings
from backend.app.ai.rag.vectorstores.qdrant_store import QdrantStore




def retrieve_documents(
        query : str,
        embedding_model : OpenRouterEmbeddings,
        vector_store : QdrantStore,
        limit : int = 5,
        score_threshold : float | None = None
)-> list[Document]:

    if not query:
        raise ValueError(
            "Query cannot be empty"
        )

    query_vector = embedding_model.embed_query(query)

    results = vector_store.search(
        query_vector=query_vector,
        limit=limit,
        score_threshold=score_threshold,
    )

    documents = []

    for result in results:
        payload = result.payload or {}

        metadata = {
            key:value
            for key,value in payload.items()
            if key != "text"
        }

        metadata["score"] = result.score

        documents.append(
            Document(
                page_content=payload.get("text",""),
                metadata=metadata,
            )
        )

    return documents