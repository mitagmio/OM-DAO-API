from decimal import Decimal
from typing import Optional

from app import schemas
from app.config.settings import settings


class FrameworkAdapter:
    @staticmethod
    def http_exception_400(detail): ...

    @staticmethod
    def http_exception_200(detail): ...


class BlockchainAdapter:
    def get_latest_block_number(self) -> int: ...

    def get_block_transactions(self, block_number: int) -> Optional[list[schemas.Transaction]]: ...

    def decode_input(self, input_data: str) -> Optional[schemas.DecodedInput]: ...

    def get_whitelisted_symbols(self) -> list[str]: ...

    def get_infl_token_size(self, referal_code: str, symbol: str) -> int: ...

    def get_transactions_by_events(self, from_block: int, to_block: int) -> list[schemas.Transaction]: ...


class BlockchainStorage:
    def get_last_block_number(self) -> Optional[int]: ...

    def get_transactions(self, referal_code: str, symbol: str) -> list[schemas.Transaction]: ...

    def add_transactions(self, block_number: int, transactions: list[schemas.Transaction]) -> None: ...


class TokensUseCase:
    def __init__(self, **kwargs):
        self.framework_adapter: FrameworkAdapter = kwargs.get('framework_adapter')
        self.blockchain_adapter: BlockchainAdapter = kwargs.get('blockchain_adapter')
        self.blockchain_storage: BlockchainStorage = kwargs.get('blockchain_storage')
        self.start_block_number = settings.start_block_number
        self.contract_address = settings.contract_address
        self.batch_size = settings.batch_size

    def update_transactions(self) -> None:
        last_scanned_block = self.blockchain_storage.get_last_block_number()
        block_from = last_scanned_block + 1 if last_scanned_block else self.start_block_number
        latest_block = self.blockchain_adapter.get_latest_block_number()
        block_to = block_from + self.batch_size - 1

        while True:
            if block_from > latest_block:
                break
            if block_to > latest_block:
                block_to = latest_block

            transactions = self.blockchain_adapter.get_transactions_by_events(block_from, block_to)
            print(f'Blocks #{block_from} - #{block_to} in progress')
            self.blockchain_storage.add_transactions(block_to, transactions)

            block_from += self.batch_size
            block_to += self.batch_size

    async def get_sold_tokens(self, referal_code: str) -> list[schemas.Token]:
        symbols = self.blockchain_adapter.get_whitelisted_symbols()
        tokens = []
        for symbol in symbols:
            amount = Decimal(
                self.blockchain_adapter.get_infl_token_size(referal_code, symbol) / 1000000
            ).quantize(Decimal('0.000001'))
            tokens.append(schemas.Token(symbol=symbol, amount=amount))
        return tokens

    async def get_transactions(self, referal_code: str, symbol: str) -> list[schemas.Transaction]:
        return self.blockchain_storage.get_transactions(referal_code, symbol)

    async def get_last_scanned_block_number(self) -> dict:
        return {'lastScannedBlock': self.blockchain_storage.get_last_block_number()}
