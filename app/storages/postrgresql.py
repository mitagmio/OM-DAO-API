from typing import Optional

from sqlalchemy.orm import Session

from app import schemas, models
from app.services import BlockchainStorage


class PostgresqlStorage(BlockchainStorage):
    def __init__(self, db: Session):
        self.db = db

    def _get_last_block_number_config(self) -> Optional[models.Config]:
        return self.db.query(models.Config).filter(models.Config.data['name'].astext.like('last_block_number')).first()

    def get_last_block_number(self) -> Optional[int]:
        db_config = self._get_last_block_number_config()
        if db_config:
            return db_config.data['value']
        else:
            return None

    def get_transactions(self, referal_code: str, symbol: str) -> list[schemas.Transaction]:
        db_transactions = (
            self.db.query(models.Transaction)
                .filter(models.Transaction.data['event_args']['referal_code'].astext.like(referal_code),
                        models.Transaction.data['event_args']['symbol'].astext.like(symbol))
                .all()
        )
        return [schemas.Transaction.parse_obj(db_transaction.data) for db_transaction in db_transactions]

    def add_transactions(self, block_number: int, transactions: list[schemas.Transaction]) -> None:
        if transactions:
            db_transactions = [
                models.Transaction(data=transaction.dict(exclude_none=True)) for transaction in transactions
            ]
            self.db.add_all(db_transactions)
        db_config = self._get_last_block_number_config()
        if db_config:
            config = schemas.Config.parse_obj(db_config.data)
            config.value = block_number
            db_config.data = config.dict()
        else:
            config_data = schemas.Config(name='last_block_number', value=block_number)
            self.db.add(models.Config(data=config_data.dict()))
        self.db.commit()
