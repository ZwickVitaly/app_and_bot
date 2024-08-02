from contextlib import asynccontextmanager

from settings import logger


@asynccontextmanager
async def basic_lifespan(*args, **kwargs):
    logger.debug("Starting application")
    logger.info("Application started working")
    yield
    logger.info("Shutting down app")
