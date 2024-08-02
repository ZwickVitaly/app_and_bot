from os import getenv
from sys import stdout

from loguru import logger

DOCKER = getenv("DOCKER_ENV", "0") == "1"
DEBUG = (getenv("DEBUG", "0") == "1") if not DOCKER else True
DB_HOST = "mongo" if DOCKER else "localhost"

MONGO_USER = getenv("MONGO_USER")
MONGO_PASSWORD = getenv("MONGO_PASSWORD")
MESSAGES_COLLECTION_NAME = getenv("MESSAGES_COLLECTION_NAME") or "messages"

PAGE_SIZE = int(getenv("PAGE_SIZE", "20"))
if PAGE_SIZE < 1:
    raise ValueError("PAGE_SIZE can't be lower than 1")

TOTAL_PAGES_KEY = getenv("TOTAL_PAGES_KEY", "total_pages")

if MESSAGES_COLLECTION_NAME == TOTAL_PAGES_KEY:
    raise ValueError("TOTAL_PAGES_KEY and MESSAGES_COLLECTION_NAME cannot be same")

MESSAGE_MAX_LEN = int(getenv("MESSAGE_MAX_LEN", "300"))
if MESSAGE_MAX_LEN < 1:
    raise ValueError("MESSAGE_MAX_LEN must be above 0")

if any((MESSAGES_COLLECTION_NAME == "cache", TOTAL_PAGES_KEY == "cache")):
    raise ValueError("MESSAGES_COLLECTION_NAME or TOTAL_PAGES_KEY should not be equal to 'cache'")

logger.remove()
logger.add(
    "logs/debug_logs.log" if DEBUG else "logs/bot.log",
    rotation="00:00:00",
    level="DEBUG" if DEBUG else "INFO",
)
if DEBUG:
    logger.add(stdout, level="DEBUG")
