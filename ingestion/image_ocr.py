import easyocr


reader = easyocr.Reader(['en','hi'])


def extract_text_from_image(file_path):
    """
    Extract text from image using OCR.
    """

    results = reader.readtext(file_path)

    extracted_text = ""

    for result in results:
        extracted_text += result[1] + " "

    return extracted_text