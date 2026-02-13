from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_MODEL = os.getenv("GENAI_MODEL", "gemini-2.5-flash")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
