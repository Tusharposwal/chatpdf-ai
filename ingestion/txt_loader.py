def extract_text_from_txt(file_path):
    """
    Extract text from TXT file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text