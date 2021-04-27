from random import randint


async def send_message(text, pk, VK_API):
    await VK_API.messages.send(
        user_id=pk,
        message=text,
        random_id=randint(-2147483648, +2147483647),
    )

