from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    DATA_DIR: str = "data"

settings = Settings()
