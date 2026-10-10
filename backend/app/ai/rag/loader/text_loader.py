from pathlib import Path
from langchain_core.documents import Document


def load_text_file(file_path:str | Path) -> Document:

    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    if not path.is_file():
        raise ValueError(f"path is not a file: {path}")

    text = path.read_text(encoding="utf-8")

    document = Document(
        page_content=text,
        metadata={
            "source": str(path),
            "file_type":path.suffix.lower().lstrip(".",)
        },
    )

    return document

if __name__ == "__main__":
    doc = load_text_file('backend/app/ai/rag/data/company.txt')

    print(doc.page_content)
    print(doc.metadata)