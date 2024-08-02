from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.filters import CommandStart, Command

from settings import (
    BASE_WEBHOOK_URL,
    WEBHOOK_PATH,
    BOT_TOKEN,
    WEB_SERVER_HOST,
    WEB_SERVER_PORT,
    logger
)
from handlers import start_command_handler, get_messages_command_handler, new_message_command_handler


async def on_startup(bot: Bot) -> None:
    logger.warning(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")
    await bot.set_webhook(f"https://{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")


def main_webhooks():
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.message.register(start_command_handler, CommandStart())
    dp.message.register(get_messages_command_handler, Command('messages'))
    dp.message.register(new_message_command_handler, Command('new_message'))

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    logger.info("Bot turning on")
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    logger.info("Bot is off")
