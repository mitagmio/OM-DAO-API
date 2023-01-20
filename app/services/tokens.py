from typing import Optional

from app import schemas
from app.config.settings import settings


class FrameworkAdapter:
    @staticmethod
    def http_exception_400(detail): ...

    @staticmethod
    def http_exception_200(detail): ...


class BlockchainAdapter:
    def get_block_transactions(self, block_number: int) -> Optional[list[schemas.Transaction]]: ...

    def decode_input(self, input_data: str) -> Optional[schemas.DecodedInput]: ...

    def get_whitelisted_symbols(self) -> list[str]: ...

    def get_infl_token_size(self, referal_code: str, symbol: str) -> int: ...


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

    def update_transactions(self) -> None:
        last_block_number = self.blockchain_storage.get_last_block_number()
        block_number = last_block_number + 1 if last_block_number else self.start_block_number

        while True:
            transactions = self.blockchain_adapter.get_block_transactions(block_number)
            if transactions is None:
                break

            print(f'Block #{block_number} in progress')

            discovered_transactions = []
            for transaction in transactions:
                if transaction.to_address == self.contract_address:
                    transaction.decoded_input = self.blockchain_adapter.decode_input(transaction.input)
                    discovered_transactions.append(transaction)

            self.blockchain_storage.add_transactions(block_number, discovered_transactions)
            block_number += 1

    async def get_sold_tokens(self, referal_code: str) -> list[schemas.Token]:
        symbols = self.blockchain_adapter.get_whitelisted_symbols()
        tokens = []
        for symbol in symbols:
            token = schemas.Token(
                symbol=symbol,
                amount=self.blockchain_adapter.get_infl_token_size(referal_code, symbol)
            )
            tokens.append(token)
        return tokens

    async def get_transactions(self, referal_code: str, symbol: str) -> list[schemas.Transaction]:
        return self.blockchain_storage.get_transactions(referal_code, symbol)
