from langchain_chroma import Chroma

from rag.embeddings import load_embedding_model


CHROMA_DB_DIR = "storage/chroma_db"


def get_vector_store():

    embedding_model = load_embedding_model()

    vector_store = Chroma(
        collection_name="chatpdf_collection",
        embedding_function=embedding_model,
        persist_directory=CHROMA_DB_DIR
    )

    return vector_store


def store_chunks(
    chunks,
    source_name,
    user_id
):
    """
    Store chunks with metadata.
    Replace old vectors if document already exists.
    """

    # Delete existing vectors of same document
    delete_document_vectors(
        user_id=user_id,
        document_name=source_name
    )

    vector_store = get_vector_store()

    documents = []
    metadatas = []
    ids = []

    for index, chunk_data in enumerate(chunks):

        documents.append(
            chunk_data["text"]
        )

        metadatas.append({
            "source": source_name,
            "chunk_id": index,
            "page": chunk_data["page"],
            "user_id": user_id
        })

        ids.append(
            f"{user_id}_{source_name}_{index}"
        )

    vector_store.add_texts(
        texts=documents,
        metadatas=metadatas,
        ids=ids
    )


def get_retriever(user_id):
    """
    Multi-document retriever.
    Searches across all user documents.
    """

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 6,
            "filter": {
                "user_id": user_id
            }
        }
    )

    return retriever


def delete_document_vectors(
    user_id,
    document_name
):

    """
    Delete vectors related to a document.
    """

    vector_store = get_vector_store()

    results = vector_store.get(
        where={
            "$and": [
                {"user_id": user_id},
                {"source": document_name}
            ]
        }
    )

    if not results or not results["ids"]:
        return

    vector_store.delete(
        ids=results["ids"]
    )
    