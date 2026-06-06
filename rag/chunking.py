from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def chunk_text(document_data):
    """
    Create chunks with metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunked_documents = []

    # PDF
    if document_data["type"] == "pdf":

        for page_data in document_data["content"]:

            page_number = page_data["page"]

            page_text = page_data["text"]

            chunks = splitter.split_text(page_text)

            for chunk in chunks:

                chunked_documents.append({
                    "text": chunk,
                    "page": page_number
                })

    # Other files
    else:

        chunks = splitter.split_text(
            document_data["content"]
        )

        for chunk in chunks:

            chunked_documents.append({
                "text": chunk,
                "page": None
            })

    return chunked_documents