from controllers import api_message_router, api_messages_router
from fastapi import FastAPI
from lifespan import basic_lifespan
from settings import logger

logger.debug("Init FastAPI")
app = FastAPI(lifespan=basic_lifespan)

# Plugging in routers
logger.debug("Plugging routers")
app.include_router(api_messages_router, prefix="/api/v1")
app.include_router(api_message_router, prefix="/api/v1")
