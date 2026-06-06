from vectordb.vector_store import get_retriever


def retrieve_chunks(
    query,
    user_id
):
    """
    Retrieve chunks across all user documents.
    """

    retriever = get_retriever(user_id)

    retrieved_docs = retriever.invoke(query)

    return retrieved_docs