import json
from typing import Optional

from web3 import Web3

from app import schemas
from app.config.settings import settings
from app.services import BlockchainAdapter


class Web3Adapter(BlockchainAdapter):
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(settings.infura_url + settings.infura_api_key))
        with open('app/config/abi/omd_abi.json') as json_file:
            ABI = json.load(json_file)
        self.contract = self.web3.eth.contract(settings.contract_address, abi=ABI)

    @staticmethod
    def _str_to_bytes32(value: str) -> bytes:
        bytes_value = value.encode()
        while len(bytes_value) < 32:
            bytes_value += b'\x00'
        return bytes_value

    @staticmethod
    def _bytes32_to_str(value: bytes) -> str:
        str_value = value.decode('utf-8')
        str_value = str_value.replace('\x00', '')
        return str_value

    def get_block_transactions(self, block_number: int) -> Optional[list[schemas.Transaction]]:
        try:
            block = self.web3.eth.get_block(block_number, full_transactions=True)
            if not block:
                return None
            if not block['transactions']:
                return []
            transactions = []
            for block_transaction in block['transactions']:
                if block_transaction:
                    transaction = schemas.Transaction.parse_obj(block_transaction)
                    transaction.timestamp = block['timestamp']
                    transactions.append(transaction)
            return transactions
        except:
            return []

    def decode_input(self, input_data: str) -> Optional[schemas.DecodedInput]:
        try:
            f, decoded_input_data = self.contract.decode_function_input(input_data)
            return schemas.DecodedInput(
                symbol=self._bytes32_to_str(decoded_input_data['symbol']),
                amount=decoded_input_data['_amount'],
                referal_code=self._bytes32_to_str(decoded_input_data['referalCode'])
            )
        except:
            return None

    def get_whitelisted_symbols(self) -> list[str]:
        symbols = self.contract.functions.getWhitelistedSymbols().call()
        return [self._bytes32_to_str(symbol) for symbol in symbols]

    def get_infl_token_size(self, referal_code: str, symbol: str) -> int:
        return self.contract.functions.getInflTokenSize(
            self._str_to_bytes32(referal_code),
            self._str_to_bytes32(symbol)
        ).call()
