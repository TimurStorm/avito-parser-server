import os
from sanic import Sanic
from dotenv import load_dotenv

APP = Sanic("app")

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    p = load_dotenv(dotenv_path)

IP = os.getenv("IP", default="0.0.0.0")
PORT = os.getenv("PORT", default=8000)

VK_TOKEN = os.getenv("VK_TOKEN")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
