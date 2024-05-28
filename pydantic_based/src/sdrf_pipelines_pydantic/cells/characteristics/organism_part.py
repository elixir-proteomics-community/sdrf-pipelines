from pydantic import BaseModel, Field

class Organismpart(BaseModel):
    value: str = Field(..., alias='characteristics[organism part]')