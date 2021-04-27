import aiovk
from aiovk.drivers import HttpDriver
from sanic.response import json
from src.main.methods import send_message
from src.main.settings import VK_TOKEN


def setup_routes(app):

    @app.listener("after_server_start")
    def get_api(app, loop):
        global VK_API
        VK_API = aiovk.API(
            aiovk.TokenSession(
                VK_TOKEN,
                driver=HttpDriver(loop=loop),
            )
        )

    @app.post("/vk")
    async def foo_handler(request):
        try:
            app.add_task(
                send_message(
                    request.args['tx'][0],
                    request.args['id'][0],
                    VK_API
                )
            )
            return json({"text": "Everything is okay"}, status=200)
        except Exception as error:
            return json({"error": str(error)}, status=500)