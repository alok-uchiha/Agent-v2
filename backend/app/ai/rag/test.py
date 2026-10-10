from langchain_core.documents import Document
from backend.app.ai.rag.pipeline.context_builder import build_context

documents = [
    Document(
        page_content="Standard shipping takes 5–7 business days.",
        metadata={
            "source": "company.txt",
            "header_2": "Shipping Policy",
            "score": 0.72,
        },
    ),
    Document(
        page_content="Refunds can be requested within 30 days.",
        metadata={
            "source": "company.txt",
            "header_2": "Refund Policy",
            "score": 0.61,
        },
    ),
]

print(build_context(documents))