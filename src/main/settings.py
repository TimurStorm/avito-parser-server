import os
from sanic import Sanic
from dotenv import load_dotenv
import vk_api

app = Sanic("app")


def get_api(token):
    session = vk_api.VkApi(token=token)
    return session.get_api()


dotenv_path = os.path.join(os.path.dirname(__file__), "local.env")
if os.path.exists(dotenv_path):
    p = load_dotenv(dotenv_path)

IP = os.getenv("IP", default="0.0.0.0")
PORT = os.getenv("PORT", default=8000)
VK_TOKEN = os.getenv("VK_TOKEN")
VK_API = get_api(VK_TOKEN)
