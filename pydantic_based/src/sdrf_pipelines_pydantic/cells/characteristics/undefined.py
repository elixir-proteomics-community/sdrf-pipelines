from pydantic import BaseModel, Field


class Undefined(BaseModel):
    value: str = Field(..., alias="characteristics[organism disease]")
