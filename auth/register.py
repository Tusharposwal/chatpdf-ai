from database.supabase_client import supabase
from auth.auth_utils import hash_password

def register_user(
    username,
    password
):
    """
    Register new user.
    """

    # Hash password
    hashed_password = hash_password(password)

    try:

        existing_user = (
            supabase.table("users").select("id").eq("username", username).execute()
        )

        if existing_user.data:

            return False

        (
            supabase.table("users")
            .insert({"username": username, "password": hashed_password})
            .execute()
        )

        return True

    except Exception as e:

        print(f"Register Error: {e}")

        return False
