from pydantic import BaseModel, Field

class Organism(BaseModel):
    value: str = Field(..., alias='characteristics[organism]')