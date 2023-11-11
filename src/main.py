import uvicorn

from core.config import settings
from core.models import Base
from core.db_helper import db_helper
from api_v1 import router as router_v1
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


def create_app():
    app = FastAPI(lifespan=lifespan,title='Pharmacy REST API')
    app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
    return app

if __name__ == '__main__':
    uvicorn.run('main:create_app', factory=True, reload=True, port=8000)