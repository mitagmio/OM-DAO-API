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
    """
    Returns sold tokens by referal code.

    Args:
        referal_code (str): referal code;
        use_case (TokensUseCase, optional): tokens use case business logic. Defaults to Depends(get_tokens_use_case).
    Returns:
        list[schemas.Token]: token list.
    """
    return await use_case.get_sold_tokens(referal_code)


@router.get("/transactions")
async def get_transactions(
        referal_code: str,
        symbol: str,
        use_case: TokensUseCase = Depends(get_tokens_use_case)
) -> list[schemas.Transaction]:
    """
    Returns transactions by referal code and symbol.

    Args:
        referal_code (str): referal code;
        symbol (str): symbol;
        use_case (TokensUseCase, optional): tokens use case business logic. Defaults to Depends(get_tokens_use_case).
    Returns:
        list[schemas.Transaction]: transaction list.
    """
    return await use_case.get_transactions(referal_code, symbol)


@router.get("/last_scanned_block")
async def last_scanned_block(
        use_case: TokensUseCase = Depends(get_tokens_use_case)
) -> dict:
    """
    Returns number of last background scanned block.

    Args:
        use_case (TokensUseCase, optional): tokens use case business logic. Defaults to Depends(get_tokens_use_case).
    Returns:
        dict: number of last scanned block.
    """
    return await use_case.get_last_scanned_block_number()
