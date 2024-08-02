from pydantic import BaseModel, Field


class PageSchema(BaseModel):
    page: int = Field(ge=1, default=1)
