import os

from vectordb.vector_store import delete_document_vectors

from database.supabase_client import supabase


def save_document(user_id, document_name):
    """
    Save uploaded document.
    Prevent duplicate entries.
    """

    try:

        existing = (
            supabase.table("documents")
            .select("id")
            .eq("user_id", user_id)
            .eq("document_name", document_name)
            .execute()
        )

        if not existing.data:

            (
                supabase.table("documents")
                .insert({"user_id": user_id, "document_name": document_name})
                .execute()
            )

    except Exception as e:

        print(f"Save Document Error: {e}")


def get_user_documents(user_id):
    """
    Get all documents of current user.
    """

    try:

        response = (
            supabase.table("documents")
            .select("document_name")
            .eq("user_id", user_id)
            .order("id", desc=True)
            .execute()
        )

        return [row["document_name"] for row in response.data]

    except Exception as e:

        print(f"Get Documents Error: {e}")

        return []


def delete_document(user_id, document_name):
    """
    Delete document and related chats.
    """

    try:

        (
            supabase.table("documents")
            .delete()
            .eq("user_id", user_id)
            .eq("document_name", document_name)
            .execute()
        )

        (
            supabase.table("chats")
            .delete()
            .eq("user_id", user_id)
            .eq("document_name", document_name)
            .execute()
        )

        delete_document_vectors(user_id, document_name)

        file_path = os.path.join("uploads", document_name)

        if os.path.exists(file_path):

            os.remove(file_path)

    except Exception as e:

        print(f"Delete Document Error: {e}")
