from math import ceil

from aiogram.types import Message
from settings import logger, MESSAGES_COLLECTION_NAME, MESSAGE_MAX_LEN, PAGE_SIZE, TOTAL_PAGES_KEY
from datetime import datetime
from utils import mongo_db, redis_db


async def new_message_command_handler(message: Message):
    await message.delete()
    logger.debug(f"Пользователь {message.from_user.id} запросил команду {message.text}")
    try:
        message_text = message.text.replace("/new_message", "", 1).strip()
        if not message_text:
            await message.answer("Сообщение не может быть пустым!")
            return
        if len(message_text) > MESSAGE_MAX_LEN:
            await message.answer(f"Сообщение не должно быть длинее {MESSAGE_MAX_LEN} символов")
            return
        new_message = {
            "message_text": message_text,
            "author_username": message.from_user.username or message.from_user.full_name,
            "created_at": datetime.now(),
            "telegram_id": message.from_user.id,
        }
        message_collection = mongo_db.get_collection(MESSAGES_COLLECTION_NAME)
        message_collection.insert_one(new_message)
        collection_length = message_collection.estimated_document_count()
        total_pages = ceil(collection_length / PAGE_SIZE)
        await redis_db.set(TOTAL_PAGES_KEY, total_pages)
        await redis_db.delete("cache")
        await message.answer("Сообщение отправлено!")
    except Exception as e:
        logger.error(e)
        await message.answer("Упс :( что-то пошло не так.")
