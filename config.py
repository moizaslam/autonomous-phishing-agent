import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    HF_API_TOKEN = os.getenv("HF_API_TOKEN")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 993))
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
