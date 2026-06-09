import gc
import fitz

from ingestion.image_ocr import extract_text_from_pixmap


def extract_text_from_pdf(file_path):
    """
    Extract page-wise text from PDF.
    Uses Gemini Vision as OCR fallback for scanned pages.
    """

    doc = fitz.open(file_path)
    pages = []

    try:
        for page_number, page in enumerate(doc):

            text = page.get_text().strip()

            if len(text) < 50:
                try:
                    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                    try:
                        ocr_text = extract_text_from_pixmap(pix)
                        if ocr_text.strip():
                            text = ocr_text
                    finally:
                        del pix
                        gc.collect()

                except Exception as e:
                    print(f"OCR failed on page {page_number + 1}: {e}")

            pages.append({"page": page_number + 1, "text": text})

    finally:
        doc.close()

    return pages
