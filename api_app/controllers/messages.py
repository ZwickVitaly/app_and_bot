import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from schemas import FeedOutSchema, PageSchema
from settings import MESSAGES_COLLECTION_NAME, PAGE_SIZE, TOTAL_PAGES_KEY, logger
from utils import mongo_db, redis_db

api_messages_router = APIRouter(prefix="/messages", tags=["messages"])


@api_messages_router.get(
    "",
    responses={
        200: {"model": FeedOutSchema},
    },
)
async def get_messages_handler(request: Request, page: PageSchema = Depends()):
    total_pages: int = await redis_db.get(TOTAL_PAGES_KEY) or 0
    if total_pages and int(total_pages) < page.page:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Page not found{', database is empty.' if not total_pages else ''}"
            },
        )
    if page.page == 1:
        cache = await redis_db.get("cache")
        if cache:
            j = json.loads(cache)
            return j
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
                "created_at": {
                    "$dateToString": {
                        "format": "%H:%M:%S %d.%m.%Y",
                        "date": "$created_at",
                    }
                },
            }
        },
    ]
    if page.page - 1:
        pipe.insert(1, {"$skip": PAGE_SIZE * (page.page - 1)})
    try:
        result = list(mongo_collection.aggregate(pipe))
        result_schema = FeedOutSchema(messages=result)
        if page.page == 1:
            await redis_db.set("cache", result_schema.model_dump_json())
        return result_schema
    except Exception as e:
        logger.error(f"{e}")
        return JSONResponse(status_code=500, content={"detail": "WHOOPSIE :("})
