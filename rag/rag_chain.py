from llm.gemini_client import load_gemini_model

from rag.hybrid_retriever import hybrid_search

from rag.reranker import rerank_documents


def format_chat_history(chat_history):

    history = ""

    for message in chat_history:

        role = message["role"]

        content = message["content"]

        history += f"{role}: {content}\n"

    return history


def generate_rag_response(
    question, user_id, chat_history=None, selected_documents=None
):
    """
    Generate streaming RAG response
    with hybrid retrieval + reranking.
    """

    # ---------------- HYBRID RETRIEVAL ---------------- #

    retrieved_docs = hybrid_search(
        query=question, user_id=user_id, selected_documents=selected_documents, top_k=10
    )

    # ---------------- RERANKING ---------------- #

    retrieved_docs = rerank_documents(query=question, documents=retrieved_docs, top_k=8)

    # ---------------- BUILD CONTEXT ---------------- #

    context = ""

    for doc in retrieved_docs:

        source = doc.metadata.get("source", "Unknown")

        page = doc.metadata.get("page", "N/A")

        context += f"""
        
        Document: {source}
        Page: {page}
{doc.page_content}

"""

    # ---------------- CHAT HISTORY ---------------- #

    history_text = ""

    if chat_history:

        recent_history = chat_history[-20:]
        history_text = format_chat_history(recent_history)

    # ---------------- PROMPT ---------------- #

    prompt = f"""
You are an AI assistant for document question answering.

STRICT RULES:

1. Answer only using information found in the provided document context.

2. If the answer cannot be found in the context, respond exactly:

I could not find this information in the uploaded documents.

3. Do not use external knowledge.

4. Use conversation history for continuity.

5. When information comes from multiple documents, combine it clearly.

6. Be concise and factual.

If multiple documents appear in the context:

- Mention all relevant documents.
- Summarize each document separately when asked.
- Compare documents when appropriate.

Conversation History:
{history_text}

Document Context:
{context}

Question:
{question}

Answer:
"""

    # ---------------- GEMINI ---------------- #

    model = load_gemini_model()

    # STREAMING RESPONSE
    response_stream = model.generate_content(prompt, stream=True)

    return {"stream": response_stream, "sources": retrieved_docs}
