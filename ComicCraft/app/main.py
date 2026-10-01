from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR, settings
from app.routes import router


app = FastAPI(
    title=settings.app_name,
    description="ComicCraft - AI Comic Story Creator",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


app.include_router(router)