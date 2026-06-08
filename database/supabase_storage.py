from database.supabase_client import supabase

BUCKET_NAME = "documents"


def upload_file_to_storage(local_file_path, storage_file_name, user_id):
    """
    Upload file to Supabase Storage.
    """

    try:

        with open(local_file_path, "rb") as file:

            file_data = file.read()

        response = supabase.storage.from_(BUCKET_NAME).upload(
            path=f"user_{user_id}/{storage_file_name}",
            file=file_data,
            file_options={"upsert": "true"},
        )

    except Exception as e:

        print("UPLOAD ERROR:")
        print(type(e))
        print(e)

        raise


def delete_file_from_storage(storage_file_name, user_id):
    """
    Delete file from Supabase Storage.
    """

    supabase.storage.from_(BUCKET_NAME).remove([f"user_{user_id}/{storage_file_name}"])


def download_file_from_storage(storage_file_name, local_file_path, user_id):
    """
    Download file from Supabase Storage.
    """

    data = supabase.storage.from_(BUCKET_NAME).download(
        f"user_{user_id}/{storage_file_name}"
    )
    with open(local_file_path, "wb") as file:

        file.write(data)


def list_files_in_storage():
    """
    List all files in bucket.
    """

    try:

        files = supabase.storage.from_(BUCKET_NAME).list()

        return files

    except Exception as e:

        print(f"List files error: {e}")

        return []
