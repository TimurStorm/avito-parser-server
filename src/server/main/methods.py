from random import randint


async def send_message(text, pk, api):
    try:
        await api.messages.send(
            user_id=pk, message=text, random_id=randint(-2147483648, +2147483647)
        )
    except Exception as error:
        return error
