from sanic.response import json
from methods import send_message
import aiovk
from aiovk.drivers import HttpDriver


def get_api(app):
    return aiovk.API(
        aiovk.TokenSession(
            "165a143791d5431d7b9a3e628b7baaaa7fcaaac794da2bd3ed97c9e1f0c64e6a65bed9508541ea8a3a2c5",
            driver=HttpDriver(loop=app.loop),
        )
    )


def setup_routes(app):
    @app.post("/vk")
    async def foo_handler(request):
        VK_API = get_api(app)
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