from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters import FastapiAdapter, Web3Adapter
from app.config.database import SessionLocal

from app.services.tokens import TokensUseCase
from app.storages import PostgresqlStorage


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_tokens_use_case(db: Session = Depends(get_db)) -> TokensUseCase:
    return TokensUseCase(
        blockchain_storage=PostgresqlStorage(db),
        blockchain_adapter=Web3Adapter(),
        framework_adapter=FastapiAdapter()
    )
