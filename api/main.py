from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import items, users
from core.conf import settings

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def home():
    return {'Важное сообщение': 'Привет друг! Изучать апи это весело ;)'}

app.include_router(items.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
