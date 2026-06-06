from database.supabase_client import supabase
from auth.auth_utils import verify_password


def login_user(username, password):
    """
    Authenticate user.
    """

    try:

        response = (
            supabase.table("users").select("*").eq("username", username).execute()
        )

        users = response.data

        if not users:

            return None

        user = users[0]

        stored_password = user["password"]

        if verify_password(password, stored_password):

            return user["id"]

        return None

    except Exception as e:

        print(f"Login Error: {e}")

        return None
