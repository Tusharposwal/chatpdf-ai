import fitz
import numpy as np

from ingestion.image_ocr import get_reader


def extract_text_from_pdf(file_path):
    """
    Extract page-wise text from PDF.
    Uses OCR fallback for scanned pages.
    """

    doc = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(doc):

        text = page.get_text().strip()

        # If page contains little text,
        # assume it may be scanned.
        if len(text) < 50:

            try:

                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

                image = np.frombuffer(pix.samples, dtype=np.uint8)

                image = image.reshape(pix.height, pix.width, pix.n)

                reader = get_reader()

                ocr_results = reader.readtext(image, detail=0)

                ocr_text = " ".join(ocr_results)

                if ocr_text.strip():

                    text = ocr_text

            except Exception as e:

                print(f"OCR failed on page {page_number + 1}: {e}")

        pages.append({"page": page_number + 1, "text": text})

    doc.close()

    return pages
