from langchain.tools import tool

from backend.app.ai.rag.embeddings.openrouter_embedding import OpenRouterEmbeddings
from backend.app.ai.rag.vectorstores.qdrant_store import QdrantStore
from backend.app.ai.rag.pipeline.retrieve import retrieve_documents
from backend.app.ai.rag.pipeline.context_builder import build_context



EMBEDDING_MODLE="nvidia/nemotron-3-embed-1b:free"
COLLECTION_NAME="knowledge_base"
VECTOR_SIZE=2048


@tool
def search_knowledge_base(query:str) -> str:
    """
    Search Aroku's company knowledge base for documented company information, policies, products, refunds, shipping, appointments, and other business-related facts.

Use this tool whenever a question requires company-specific information. Search using the user's question as a natural-language query.

**Search efficiently:** One search is normally sufficient. If the returned documents contain relevant information that answers the question, use that evidence to respond instead of searching again with minor variations such as "return," "returns," and "return policy."

If the results are genuinely irrelevant or insufficient, you may perform one additional search using a meaningfully different query. Do not repeatedly search for synonyms just to confirm the same information.

Distinguish between documented facts and assumptions. A refund policy does not automatically establish the full return procedure. If the knowledge base provides refund terms but no return instructions, explain that limitation clearly and do not invent missing details.

    """

    embedding_model = OpenRouterEmbeddings(
        model=EMBEDDING_MODLE,
    )

    vector_store = QdrantStore(
        collection_name=COLLECTION_NAME,
        vector_size=VECTOR_SIZE,
    )

    try:

        vector_store.ensure_collection()

        documents = retrieve_documents(
            query=query,
            embedding_model=embedding_model,
            vector_store=vector_store,
            limit=3,
            score_threshold=0.3,
        )

        return build_context(documents)

    finally:
        vector_store.close()