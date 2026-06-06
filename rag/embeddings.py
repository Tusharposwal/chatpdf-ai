from langchain_huggingface import HuggingFaceEmbeddings


# Global cache
embedding_model = None


def load_embedding_model():
    """
    Load embedding model only once.
    """

    global embedding_model

    if embedding_model is None:

        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

    return embedding_model
def generate_embeddings(chunks):
    """
    Generate embeddings for text chunks.
    """

    model = load_embedding_model()

    embeddings = model.embed_documents(chunks)

    return embeddings