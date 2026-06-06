from database.supabase_client import supabase


def save_message(role, message, document_name, user_id):

    try:

        (
            supabase.table("chats")
            .insert(
                {
                    "role": role,
                    "message": message,
                    "document_name": document_name,
                    "user_id": user_id,
                }
            )
            .execute()
        )

    except Exception as e:

        print(f"Chat Save Error: {e}")





def load_chat_history(document_name, user_id):

    try:

        response = (
            supabase.table("chats")
            .select("role, message")
            .eq("document_name", document_name)
            .eq("user_id", user_id)
            .order("id")
            .execute()
        )

        return [(row["role"], row["message"]) for row in response.data]

    except Exception as e:

        print(f"Chat Load Error: {e}")

        return []
