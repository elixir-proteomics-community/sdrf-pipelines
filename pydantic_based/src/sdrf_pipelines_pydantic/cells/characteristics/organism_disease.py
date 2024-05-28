from pydantic import BaseModel, Field

class OrganismDisease(BaseModel):
    value: str = Field(..., alias='characteristics[organism disease]')