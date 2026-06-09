import io
import google.generativeai as genai
from PIL import Image
from utils.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

_OCR_PROMPT = (
    "Extract all the text from this image exactly as it appears. "
    "Return only the raw text with no explanation or formatting."
)


def extract_text_from_image(file_path):
    img = Image.open(file_path)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([_OCR_PROMPT, img])
    return response.text or ""


def extract_text_from_pixmap(pix):
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([_OCR_PROMPT, img])
    return response.text or ""
