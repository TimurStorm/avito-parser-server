from aiovk import TokenSession, API
from aiovk.longpoll import BotsLongPoll
from asyncio import get_event_loop
from pprint import pprint
from src.main.methods import send_message
from settings import ID, TOKEN


async def main():
    session = TokenSession(access_token=TOKEN)
    api = API(session)
    lp = BotsLongPoll(api, ID)
    async for event in lp.iter():
        if event["type"] == "message_new":
            pprint(event)
            obj = event["object"]
            user_id = obj["user_id"]
            message = obj["body"].lower()
            start = f"""Привет! Это бот для рассылки объявлений! Здесь ты сможешь получать сообщения о новых 
            объявлениях из приложения. Ещё не устновил его? Ты можешь это сделать здесь: {
            'ссылка на скачиванивание на сайте'}"""
            # ПОЛЬЗОВАТЕЛЬ НАЖИМАЕТ ПРОДОЛЖИТЬ
            next1 = f"""Для того чтобы установить функцию рассылки необходимо:\n 
            1)Указать id аккаунта в настройках приложения и нажать кнопку "проверка"\n(твой id: {user_id})\n
            2)Ввести код подтверждения, указанный здесь """
            text = ""
            next_keyboard = """
            {
                "one_time": true,
                "buttons": [
                    [{
                    "action": {
                      "type": "text",
                      "payload": "{\\"button\\": \\"4\\"}",
                      "label": "Установить рассылку"
                    },
                    "color": "primary"
                  }]
                ]
              } """
            keyboard = None
            if message == "начать":
                keyboard = next_keyboard
                text = start
            if message == "установить рассылку":
                text = next1
            resp = await send_message(api=api, pk=user_id, text=text, keyboard=keyboard)
            if resp is not None:
                print(f"ERROR: {resp}")


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
