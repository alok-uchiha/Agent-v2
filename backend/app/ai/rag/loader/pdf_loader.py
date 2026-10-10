from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document

def load_pdf_file(file_path : str | Path) -> Document:

    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    if not path.is_file():
        raise ValueError(f"path is not a file: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f'Expected A PDF file: {path}')

    reader = PdfReader(str(path))

    documents = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        if not text.strip():
            continue

        document = Document(
            page_content=text,
            metadata={
                "source":str(path),
                "file_type":"pdf",
                "page": page_number,
            },
        )

        documents.append(document)

    return documents

if __name__ == "__main__":

    docs = load_pdf_file('backend/app/ai/rag/data/aroku_company_information.pdf')

    print('Pages loaded:', len(docs)); print('First page text:', docs[0].page_content); print('Metadata:', docs[0].metadata)