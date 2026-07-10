from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["Infrastructure"])


@health_router.get("/")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
