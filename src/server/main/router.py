from aiovk.drivers import HttpDriver
from aiovk.sessions import TokenSession
from aiovk.api import API
from sanic import Blueprint

from bcrypt import checkpw

from sanic.response import json
from sanic_jwt import Initialize

from methods import send_message
from models import User
from settings import VK_TOKEN, APP
from database import write_to_db, connect_to_db

CONN = None


def setup_vk_mailing():
    @APP.listener("after_server_start")
    def get_api(app, loop):
        global VK_API
        VK_API = API(
            TokenSession(
                VK_TOKEN,
                driver=HttpDriver(loop=loop),
            )
        )

    @APP.listener("after_server_start")
    async def get_connect(app, loop):
        global CONN
        CONN = await connect_to_db()

    @APP.post("/vk/send")
    async def vk_send(request):
        try:
            user_id = int(request.args["id"][0])
            text = request.args["tx"][0]
            resp = await send_message(text, user_id, VK_API)

            if resp is not None:
                resp = resp.args[0]["error_msg"]
                return json({"error": resp, "user": user_id}, status=400)

            return json({"text": "Everything is okay", "user": user_id}, status=200)

        except Exception as error:
            return json({"error": str(error)}, status=500)

    @APP.post("/login")
    async def authenticate(request, *args, **kwargs):
        email = request.args["email"][0]
        password = request.args["password"][0]

        if not email or not password:
            return json({"text": "Missing username or password."}, status=400)

        user_info = await CONN.fetch(f"SELECT * FROM users WHERE email='{email}'")

        if not user_info:
            return json({"text": "User not found."}, status=400)

        user_info = user_info[0]
        user = User(*[value for value in user_info.values()])

        if not checkpw(password=password.encode("utf-8"), hashed_password=user.password.encode("utf-8")):
            return json({"text": "Password is incorrect."}, status=400)
        return json({"text": "Everything is okay",
                     "user": {
                         "username": user.username,
                         "email": user.email,
                         "vk_id": user.vk_id
                     }}, status=200)

    Initialize(Blueprint("log"), APP, authenticate=authenticate)

    @APP.post("/reg")
    async def registration(request, *args, **kwargs):
        email = request.args["email"][0]
        password = request.args["password"][0]
        username = request.args["username"][0]

        if not email or not password or not username:
            return json({"text": "Missing email or username or password."}, status=400)
        user_info = await CONN.fetch(f"SELECT * FROM users WHERE email='{email}'")
        if not user_info:
            user = User(email=email, password=password, username=username)
            await write_to_db(conn=CONN, table="users", values=[email, password, username])

            return json({"text": "Everything is okay",
                         "user": {
                             "username": user.username,
                             "email": user.email,
                             "vk_id": user.vk_id,
                             "password": user.password
                         }}, status=200)
        else:
            return json({"text": "User with this email is exist"}, status=400)

    Initialize(Blueprint("reg"), APP, authenticate=registration)