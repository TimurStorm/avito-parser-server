from aiovk.drivers import HttpDriver
from aiovk.sessions import TokenSession
from aiovk.api import API

from sanic.response import json

from methods import send_message
from settings import VK_TOKEN, APP
from database import write_to_db, read_table_from_db, connect_to_db

from random import randint
from datetime import datetime


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
            user_id = request.args["id"][0]
            text = request.args["tx"][0]
            resp = await send_message(
                text , user_id, VK_API
            )

            if resp is not None:
                resp = resp.args[0]["error_msg"]
                return json({"error": resp, "user": user_id}, status=400)

            return json({"text": "Everything is okay", "user": user_id}, status=200)

        except Exception as error:
            return json({"error": str(error)}, status=500)

    @APP.post("/vk/prot1")
    async def vk_protect(request):
        """
        ЗАПИСЬ В БД КОДА И ПОЛЬЗОВАТЕЛЯ
        """
        try:
            user_id = request.args["id"][0]
            code = str(randint(100000, 999999))
            resp = await send_message(
                f"Секретный код: {code}", user_id, VK_API
            )

            if resp is not None:
                resp = resp.args[0]["error_msg"]
                return json({"error": resp, "user": user_id}, status=400)

            arr = [
                int(request.args["id"][0]),
                code,
                datetime.now().strftime("%m/%d/%Y"),
            ]

            await write_to_db(conn=CONN, table="vk_requests", values=arr)
            await read_table_from_db(conn=CONN, table="vk_requests")

            return json({"text": "Everything is okay", "user": user_id}, status=200)

        except Exception as error:
            return json({"error": str(error)}, status=500)

    @APP.post("/vk/prot2")
    async def vk_protect(request):
        """
        ПРОВЕРКА В БД КОДА ПОЛЬЗОВАТЕЛЯ
        """
        try:

            user_id = request.args["id"][0]
            code = request.args["code"][0]

            rows = await CONN.fetch(f"SELECT code FROM vk_requests WHERE id='{user_id}'")
            rows = [row.get('code') for row in rows]
            if code in rows:

                resp = await send_message(
                    "Рассылка успешно установлена! Теперь ты можешь получать объявления в VK!", user_id, VK_API
                )
                await CONN.execute(f"DELETE FROM vk_requests WHERE id='{user_id}'")
                if resp is not None:
                    resp = resp.args[0]["error_msg"]
                    return json({"error": resp, "user": user_id}, status=400)
                return json({"text": "Everything is okay"}, status=200)
            else:
                resp = await send_message(
                    "Ошибка установки рассылки: неверный код", user_id, VK_API
                )
                if resp is not None:
                    resp = resp.args[0]["error_msg"]
                    return json({"error": resp, "user": user_id}, status=400)
                return json({"text": "Everything is okay", "user": user_id}, status=200)

        except Exception as error:
            return json({"error": str(error)}, status=500)
