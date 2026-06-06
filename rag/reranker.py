from sentence_transformers import CrossEncoder


# Global reranker model
reranker_model = None


def load_reranker():

    global reranker_model

    if reranker_model is None:

        reranker_model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    return reranker_model


def rerank_documents(
    query,
    documents,
    top_k=4
):
    """
    Rerank retrieved documents.
    """

    model = load_reranker()

    # Prepare query-document pairs
    pairs = []

    for doc in documents:

        pairs.append(
            (query, doc.page_content)
        )

    # Predict relevance scores
    scores = model.predict(pairs)

    # Combine docs with scores
    scored_docs = list(
        zip(documents, scores)
    )

    # Sort descending
    scored_docs.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Return top documents
    reranked_docs = [
        doc
        for doc, score in scored_docs[:top_k]
    ]

    return reranked_docs