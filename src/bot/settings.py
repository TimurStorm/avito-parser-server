import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    p = load_dotenv(dotenv_path)

ID = int(os.getenv("ID"))
TOKEN = os.getenv("TOKEN")
