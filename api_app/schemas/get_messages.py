from pydantic import BaseModel, Field

from settings import PAGE_SIZE

from .message import MessageSchema


class MessageOutSchema(MessageSchema):
    created_at: str = Field(
        title="Message creation date",
    )


class FeedOutSchema(BaseModel):
    messages: list[MessageOutSchema] = Field(
        max_length=PAGE_SIZE,
        title="Messages list",
        examples=[
            [
                {
                    "author_username": "HowdyHo",
                    "message_text": "Later, alligator",
                    "created_at": "06:14:03 05.08.2024",
                },
                {
                    "author_username": "HowdyHee",
                    "message_text": "Later, alligator",
                    "created_at": "04:14:03 04.07.2024",
                },
                {
                    "author_username": "HowdyHaa",
                    "message_text": "Later, alligator",
                    "created_at": "02:14:03 03.06.2024",
                },
                {
                    "author_username": "HowdyHii",
                    "message_text": "Later, alligator",
                    "created_at": "01:14:03 02.05.2024",
                },
                {
                    "author_username": "HowdyHey",
                    "message_text": "Later, alligator",
                    "created_at": "00:14:03 01.04.2024",
                },
            ]
        ],
    )
