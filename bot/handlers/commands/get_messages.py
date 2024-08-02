import json

from aiogram.types import Message

from settings import MESSAGES_COLLECTION_NAME, PAGE_SIZE, TOTAL_PAGES_KEY, logger
from utils import mongo_db, redis_db
from helpers import form_page


async def get_messages_command_handler(message: Message):
    await message.delete()
    logger.debug(f"Пользователь {message.from_user.id} запросил команду {message.text}")
    total_pages: int = await redis_db.get(TOTAL_PAGES_KEY) or 0
    try:
        page = int(message.text.strip("/messages").strip())
        if page <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Количество страниц должно быть числом больше нуля. Показываю первую страницу.")
        page = 1
    if total_pages and int(total_pages) < page:
        await message.answer(f"Страница не найдена{', база данных пуста.' if not total_pages else ''}")
        return
    if page == 1:
        cache = await redis_db.get("cache")
        if cache:
            j = json.loads(cache)
            message_string = await form_page(j, message.from_user.id)
            await message.answer(f"Страница: {page}\n\n{message_string}")
            return
    mongo_collection = mongo_db.get_collection(MESSAGES_COLLECTION_NAME)
    pipe = [
        {
            "$sort": {"created_at": -1},
        },
        {
            "$limit": PAGE_SIZE,
        },
        {
            "$project": {
                "_id": 0,
                "author_username": 1,
                "message_text": 1,
                "telegram_id": 1,
                "created_at": {
                    "$dateToString": {
                        "format": "%H:%M:%S %d.%m.%Y",
                        "date": "$created_at",
                    }
                },
            }
        },
    ]
    if page - 1:
        pipe.insert(1, {"$skip": PAGE_SIZE * (page - 1)})
    try:
        messages = list(mongo_collection.aggregate(pipe))
        message_string = await form_page(messages, message.from_user.id)
        if page == 1:
            await redis_db.set("cache", json.dumps(messages))
        await message.answer(f"Страница: {page}\n\n{message_string}")
    except Exception as e:
        logger.error(f"{e}")
        await message.answer("Что-то пошло не так :(")