import os

from ingestion.pdf_loader import extract_text_from_pdf
from ingestion.docx_loader import extract_text_from_docx
from ingestion.txt_loader import extract_text_from_txt
from ingestion.image_ocr import extract_text_from_image


def route_file(file_path):
    """
    Route file to correct loader.
    """

    extension = os.path.splitext(file_path)[1].lower()

    # PDF
    if extension == ".pdf":

        return {
            "type": "pdf",
            "content": extract_text_from_pdf(file_path)
        }

    # DOCX
    elif extension == ".docx":

        return {
            "type": "docx",
            "content": extract_text_from_docx(file_path)
        }

    # TXT
    elif extension == ".txt":

        return {
            "type": "txt",
            "content": extract_text_from_txt(file_path)
        }

    # IMAGE OCR
    elif extension in [".png", ".jpg", ".jpeg"]:

        return {
            "type": "image",
            "content": extract_text_from_image(file_path)
        }

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )