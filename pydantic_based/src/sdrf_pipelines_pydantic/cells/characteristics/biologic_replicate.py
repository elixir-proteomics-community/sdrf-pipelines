from pydantic import BaseModel, Field

class biological_replicate(BaseModel):
    value: str = Field(..., alias='characteristics[biological replicate]')