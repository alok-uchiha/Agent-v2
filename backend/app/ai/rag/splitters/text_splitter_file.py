from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


def split_documents(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Document]:

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "header_1"),
            ("##", "header_2"),
            ("###", "header_3"),
        ],
        strip_headers=False,
    )

    chunks = []

    for document in documents:

        section_documents = markdown_splitter.split_text(
            document.page_content
        )

        for section in section_documents:
            section.metadata.update(document.metadata)

        chunks.extend(section_documents)

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )

    return recursive_splitter.split_documents(chunks)