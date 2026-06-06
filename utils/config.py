from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")

QDRANT_URL = os.getenv("QDRANT_URL")

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
