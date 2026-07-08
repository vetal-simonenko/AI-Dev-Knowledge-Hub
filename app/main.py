from fastapi import FastAPI

from app.api.router import router
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="AI Dev Knowledge Hub",
)

app.include_router(router)
