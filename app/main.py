from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from app.api.api import api_router
from app.config.database import SessionLocal
from app.config.deps import get_tokens_use_case

app = FastAPI(
    title='Test API for OM DAO'
)

origins = [
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix='/api')


@app.on_event("startup")
@repeat_every(seconds=10)
def update_transactions() -> None:
    with SessionLocal() as db:
        use_case = get_tokens_use_case(db)
        use_case.update_transactions()


@app.get("/")
def start():
    return "start"
