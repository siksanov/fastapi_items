from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code = 500,
        content={
            "сообщение": "Неожиданная ошибка сервера",
            "детали": str(exc)
        },
    )

app.include_router(items.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)

@app.get('/')
async def home():
    return {'Важное сообщение': 'Привет друг! Изучать апи это весело ;)'}


