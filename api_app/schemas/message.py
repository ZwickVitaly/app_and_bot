from pydantic import BaseModel, Field
from settings import MESSAGE_MAX_LEN


class MessageSchema(BaseModel):
    message_text: str = Field(
        min_length=1,
        max_length=MESSAGE_MAX_LEN,
        title="Message text",
        examples=["Biden go Texas!", "I might been underestimating my sleep time"],
    )
    author_username: str = Field(
        min_length=1,
        max_length=MESSAGE_MAX_LEN,
        title="Message author's username",
        examples=["John", "MEGADESTROYER3000"],
    )
