from os import getenv

from redis.asyncio import StrictRedis
from settings import DOCKER, logger

REDIS_HOST: str = getenv("REDIS_HOST") or "redis"
REDIS_PORT: str | int = getenv("REDIS_PORT") or 6379

if not DOCKER:
    REDIS_HOST = "localhost"

logger.debug("Init redis for api_app")
redis_db = StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)
