from typing import Optional

from pydantic import BaseModel, Field, root_validator


class DecodedInput(BaseModel):
    symbol: str
    amount: str = Field(alias="_amount")
    referal_code: str = Field(alias="referalCode")

    class Config:
        allow_population_by_field_name = True


class EventArgs(BaseModel):
    to_address: Optional[str] = Field(alias="to")
    amount: int
    symbol: str
    price: int
    referal_code: str = Field(alias="referalCode")

    class Config:
        allow_population_by_field_name = True


class Transaction(BaseModel):
    block_number: Optional[int] = Field(alias="blockNumber")
    hash: Optional[str] = Field(alias="transactionHash")
    timestamp: Optional[int]
    event_args: Optional[EventArgs] = Field(alias="args")

    class Config:
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def convert(cls, values):
        if 'transactionHash' in values and not isinstance(values['transactionHash'], str):
            values['transactionHash'] = values['transactionHash'].hex()
        return values
