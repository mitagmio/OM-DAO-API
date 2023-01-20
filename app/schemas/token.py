from pydantic import BaseModel


class Token(BaseModel):
    symbol: str
    amount: str
