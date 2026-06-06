from langchain_community.retrievers import BM25Retriever

from langchain_core.documents import Document

from vectordb.vector_store import get_vector_store


def hybrid_search(query, user_id, selected_documents=None, top_k=6):
    """
    Hybrid retrieval:
    Vector + BM25 keyword search
    """

    vector_store = get_vector_store()


# ---------------- VECTOR SEARCH ---------------- #

    if selected_documents:

        
    # One document selected
        if len(selected_documents) == 1:
            
            vector_results = vector_store.similarity_search(
            query=query,
            k=top_k,
            filter={"$and": [{"user_id": user_id}, {"source": selected_documents[0]}]},
        )

    # Multiple documents selected
        else:
            source_filters = [{"source": doc} for doc in selected_documents]
            
            vector_results = vector_store.similarity_search(
            query=query,
            k=top_k,
            filter={"$and": [{"user_id": user_id}, {"$or": source_filters}]},
        )
            
    else:
        vector_results = vector_store.similarity_search(

        query=query, k=top_k, filter={"user_id": user_id}
    )

    # ---------------- KEYWORD SEARCH ---------------- #

    # Fetch only current user's documents

    if selected_documents:

        # Single document selected
        if len(selected_documents) == 1:

            all_docs = vector_store.get(
                where={
                    "$and": [{"user_id": user_id}, {"source": selected_documents[0]}]
                }
            )

        # Multiple documents selected
        else:
            source_filters = [{"source": doc} for doc in selected_documents]

            all_docs = vector_store.get(
                where={"$and": [{"user_id": user_id}, {"$or": source_filters}]}
            )

    else:
        all_docs = vector_store.get(where={"user_id": user_id})

    filtered_docs = []

    for i in range(len(all_docs["documents"])):
        filtered_docs.append(
            Document(
                page_content=all_docs["documents"][i], metadata=all_docs["metadatas"][i]
            )
        )

    # BM25 Retriever
    print(f"BM25 documents loaded: {len(filtered_docs)}")
    bm25_retriever = BM25Retriever.from_documents(filtered_docs)

    keyword_results = bm25_retriever.invoke(query)

    keyword_results = keyword_results[:top_k]

    # ---------------- MERGE RESULTS ---------------- #

    merged_results = []

    seen_content = set()

    # Add vector results
    for doc in vector_results:

        if doc.page_content not in seen_content:

            merged_results.append(doc)

            seen_content.add(doc.page_content)

    # Add keyword results
    for doc in keyword_results:

        if doc.page_content not in seen_content:

            merged_results.append(doc)

            seen_content.add(doc.page_content)

    return merged_results[:top_k]
