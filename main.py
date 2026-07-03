from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.app.shared.errors import DomainError
from src.app.shared.routes import health_router
from src.core.config import settings
from src.core.database import create_db_and_tables
from src.core.exceptions import domain_exception_handler
from src.core.routes import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_exception_handler(DomainError, domain_exception_handler)

app.include_router(v1_router)
app.include_router(health_router)
