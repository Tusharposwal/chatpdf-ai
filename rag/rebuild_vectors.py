import os

from database.supabase_client import supabase

from database.supabase_storage import download_file_from_storage

from ingestion.file_router import route_file

from rag.chunking import chunk_text

from vectordb.vector_store import store_chunks

TEMP_DIR = "uploads"


def rebuild_all_vectors():

    os.makedirs(TEMP_DIR, exist_ok=True)

    documents = supabase.table("documents").select("*").execute()

    for doc in documents.data:

        user_id = doc["user_id"]

        document_name = doc["document_name"]

        local_path = os.path.join(TEMP_DIR, document_name)

        try:

            download_file_from_storage(document_name, local_path)

            document_data = route_file(local_path)

            chunks = chunk_text(document_data)

            store_chunks(chunks=chunks, source_name=document_name, user_id=user_id)

            print(f"Rebuilt: {document_name}")

            os.remove(local_path)

        except Exception as e:

            print(f"Failed rebuilding {document_name}: {e}")
