from sqlmodel import SQLModel, create_engine

from src.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.ENVIRONMENT == "development")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
