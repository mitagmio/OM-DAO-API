from pydantic import BaseModel


class Config(BaseModel):
    name: str
    value: int
