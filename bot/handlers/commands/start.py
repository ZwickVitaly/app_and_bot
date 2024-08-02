from aiogram.types import Message
from settings import logger


async def start_command_handler(message: Message):
    await message.delete()
    logger.debug(f"Пользователь {message.from_user.id} запросил команду {message.text}")
    await message.answer(
        "Привет!\n\n"
        "Чтобы написать сообщение использой команду /new_message [сообщение]\n\n"
        "Чтобы посмотреть сообщения используй команду /messages [необязательно:номер_страницы]\n"
        "Если номер страницы не будет указан (или будет указано число меньше 1) - бот покажет последнюю страницу"
    )
