import streamlit as st
import easyocr


@st.cache_resource
def get_reader():
    """
    Load OCR model only once.
    """
    return easyocr.Reader(["en", "hi"], gpu=False)


def extract_text_from_image(file_path):
    """
    Extract text from image using OCR.
    """

    reader = get_reader()

    results = reader.readtext(file_path)

    extracted_text = ""

    for result in results:
        extracted_text += result[1] + " "

    return extracted_text
