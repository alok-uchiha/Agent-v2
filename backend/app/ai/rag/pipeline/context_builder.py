from langchain_core.documents import Document



def build_context(
        doucments : list[Document]
) -> str:

    if not doucments:
        return "No relevent informantion was retrive"

    sections = []

    for index, document in enumerate(doucments, start=1):
        metadata = document.metadata

        source = metadata.get("source", "umknown source")
        section = metadata.get("header_2") or metadata.get("header_1")
        page = metadata.get("page")


        source_info = f"Source: {source}"

        if section:
            source_info += f"\nSection: {section}"

        if page is not None:
            source_info += f"\nPage: {page}"

        sections.append(
            f"[Document {index}]\n"
            f"{source_info}\n"
            f"Content:\n{document.page_content}"
        )

    return "\n\n---\n\n".join(sections)