import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from handlers import start_command_handler, get_messages_command_handler, new_message_command_handler
from settings import BOT_TOKEN, logger


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()


dp.message.register(start_command_handler, CommandStart())
dp.message.register(get_messages_command_handler, Command('messages'))
dp.message.register(new_message_command_handler, Command('new_message'))


def main_polling():
    logger.info("Bot turning on")
    asyncio.new_event_loop().run_until_complete(dp.start_polling(bot))
    logger.info("Bot is off")
