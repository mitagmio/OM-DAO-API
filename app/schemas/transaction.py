from typing import Optional

from pydantic import BaseModel, Field, root_validator


class DecodedInput(BaseModel):
    symbol: str
    amount: str = Field(alias="_amount")
    referal_code: str = Field(alias="referalCode")

    class Config:
        allow_population_by_field_name = True


class Transaction(BaseModel):
    block_number: Optional[int] = Field(alias="blockNumber")
    hash: Optional[str]
    timestamp: Optional[int]
    from_address: Optional[str] = Field(alias="from")
    to_address: Optional[str] = Field(alias="to")
    input: Optional[str] = Field(exclude=True)
    decoded_input: Optional[DecodedInput] = Field(alias="decodedInput")

    class Config:
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def convert(cls, values):
        if 'hash' in values and not isinstance(values['hash'], str):
            values['hash'] = values['hash'].hex()
        return values
