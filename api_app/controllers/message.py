from datetime import datetime
from math import ceil

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
from schemas import MessageSchema
from settings import MESSAGES_COLLECTION_NAME, PAGE_SIZE, TOTAL_PAGES_KEY, logger
from utils import mongo_db, redis_db

api_message_router = APIRouter(prefix="/message", tags=["message"])


@api_message_router.post("")
async def post_message_handler(request: Request, message: MessageSchema):
    try:
        message_dump = message.model_dump()
        logger.info(f"New message: {message_dump}")
        message_dump["created_at"] = datetime.now()
        message_collection = mongo_db.get_collection(MESSAGES_COLLECTION_NAME)
        message_collection.insert_one(message_dump)
        collection_length = message_collection.estimated_document_count()
        total_pages = ceil(collection_length / PAGE_SIZE)
        await redis_db.set(TOTAL_PAGES_KEY, total_pages)
        await redis_db.delete("cache")
        return Response(status_code=201)
    except Exception as e:
        logger.error(f"{e}")
        return JSONResponse(
            status_code=500, content={"detail": "We awe sowwy, something went wwong :("}
        )
