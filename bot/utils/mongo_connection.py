import pymongo
from pymongo import MongoClient
from settings import (
    DB_HOST,
    MESSAGES_COLLECTION_NAME,
    MONGO_PASSWORD,
    MONGO_USER,
    logger,
)

logger.debug("Init mongo for bot")
mongo_client: MongoClient = MongoClient(
    f"mongodb://{MONGO_USER or 'root'}:{MONGO_PASSWORD or 'admin123'}@{DB_HOST or 'localhost'}:27017/"
)
mongo_db = mongo_client.get_default_database(default=MESSAGES_COLLECTION_NAME)
mongo_db.get_collection(MESSAGES_COLLECTION_NAME).create_index(
    [
        ("created_at", pymongo.DESCENDING),
    ]
)