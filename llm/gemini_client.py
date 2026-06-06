import google.generativeai as genai

from utils.config import GEMINI_API_KEY


genai.configure(
    api_key=GEMINI_API_KEY
)


def load_gemini_model():

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash"
    )

    return model