from random import randint


async def send_message(text, pk, api, keyboard=None):
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
