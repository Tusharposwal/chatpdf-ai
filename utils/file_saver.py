import os


UPLOAD_DIR = "uploads"


def save_uploaded_file(uploaded_file):
    """
    Save uploaded file safely.
    Replace old file if exists.
    """

    # Create uploads folder
    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        uploaded_file.name
    )

    # Delete old file if exists
    if os.path.exists(file_path):

        os.remove(file_path)

    # Save new file
    with open(file_path, "wb") as f:

        f.write(
            uploaded_file.getbuffer()
        )

    return file_path