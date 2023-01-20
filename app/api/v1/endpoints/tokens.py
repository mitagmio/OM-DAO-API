from fastapi import APIRouter, Depends

from app import schemas
from app.config.deps import get_tokens_use_case
from app.services.tokens import TokensUseCase

router = APIRouter()


@router.get("/sold_tokens")
async def get_sold_tokens(
        referal_code: str,
        use_case: TokensUseCase = Depends(get_tokens_use_case)
) -> list[schemas.Token]:

    return await use_case.get_sold_tokens(referal_code)


@router.get("/transactions")
async def get_transactions(
        referal_code: str,
        symbol: str,
        use_case: TokensUseCase = Depends(get_tokens_use_case)
) -> list[schemas.Transaction]:

    return await use_case.get_transactions(referal_code, symbol)
