from aiovk import TokenSession, API
from aiovk.longpoll import BotsLongPoll

from sanic import json

from settings import ID, TOKEN, APP
from random import randint


async def send_message(text, pk, keyboard=None):
    try:
        if keyboard is None:
            await api.messages.send(
                user_id=pk, message=text, random_id=randint(-2147483648, +2147483647)
            )
        else:
            await api.messages.send(
                user_id=pk,
                message=text,
                random_id=randint(-2147483648, +2147483647),
                keyboard=keyboard,
            )
    except Exception as error:
        return error


async def bots_long_poll():
    lp = BotsLongPoll(api, ID)
    async for event in lp.iter():
        if event["type"] == "message_new":

            obj = event["object"]
            user_id = obj["user_id"]
            message = obj["body"].lower()

            print(f"{user_id}: {message}")

            start = f"""Привет! Это бот для рассылки объявлений! Здесь ты сможешь получать сообщения о новых 
            объявлениях из приложения. Ещё не устновил его? Ты можешь это сделать здесь: {
            'ссылка на скачиванивание на сайте'}"""
            # ПОЛЬЗОВАТЕЛЬ НАЖИМАЕТ ПРОДОЛЖИТЬ
            nextt = "Рассылка успешно установлена!"
            text = ""
            next_keyboard = """
            {
                "one_time": false,
                "buttons": [
                    [{
                    "action": {
                      "type": "text",
                      "payload": "{\\"button\\": \\"4\\"}",
                      "label": "Установить рассылку"
                    },
                    "color": "primary"
                  },
                  {
                    "action": {
                      "type": "text",
                      "payload": "{\\"button\\": \\"4\\"}",
                      "label": "Узнать id"
                    },
                    "color": "primary"
                  }]
                ]
              } """
            keyboard = next_keyboard
            if message == "начать":
                text = start
            if message == "установить рассылку":
                text = nextt
            if message == "узнать id":
                text = f"Твой id: {user_id}"
            if message in ["начать", "установить рассылку", "узнать id"]:
                resp = await send_message(pk=user_id, text=text, keyboard=keyboard)
                if resp is not None:
                    print(f"ERROR: {resp}")


def setup_router():
    @APP.listener("after_server_start")
    async def set_api(app, loop):
        session = TokenSession(access_token=TOKEN)
        global api
        api = API(session)
        APP.add_task(bots_long_poll())

    @APP.post("/send")
    async def send(request, *args, **kwargs):
        try:
            text = request.args["text"][0]
            pk = request.args["pk"][0]
            await send_message(text=text, pk=pk)
            return json({"text": "Everything okay"}, status=200)
        except Exception as e:
            print(e)
            return json({"text": "Bad request"}, status=400)
