from fastapi import APIRouter

from app.api.v1.endpoints import tokens

router = APIRouter()
router.include_router(tokens.router, prefix='/tokens', tags=['Tokens'])
