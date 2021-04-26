from sanic.response import json
from methods import send_message
from time import time
import sanic


'''def setup_routes(app):
    @app.get("/foo")
    async def foo_handler(request):
        start_time = time()
        try:
            await send_message(
                "Это тестовое сообщение с сервера. Сообщите о нём моему владельцу в кратчейшее время."
            )
            print(time() - start_time)
            return json({"text": "Everything is okay"}, status=200)
        except Exception as error:
            return json({"error": str(error)}, status=500)'''


def setup_routes(app):
    @app.get("/foo")
    async def foo_handler(request):
        start_time = time()
        send_message(
                "Это тестовое сообщение с сервера. Сообщите о нём моему владельцу в кратчейшее время."
            )
        print(time() - start_time)
        return json({"text": "Everything is okay"}, status=200)
