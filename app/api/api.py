from fastapi import APIRouter

from app.api.v1 import api

api_router = APIRouter()
api_router.include_router(api.router, prefix='/v1')
