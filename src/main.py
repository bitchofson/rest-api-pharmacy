import uvicorn

from core.config import settings
from api_v1 import router as router_v1
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app():
    app = FastAPI(lifespan=lifespan,title='Pharmacy REST API')
    app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
    return app

if __name__ == '__main__':
    uvicorn.run('main:create_app', factory=True, reload=True, port=8000)