from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.shared.errors import DomainError


async def domain_exception_handler(request: Request, exc: DomainError) -> JSONResponse:
    status_code = getattr(exc, "status_code", 400)
    return JSONResponse(status_code=status_code, content={"detail": exc.detail})
