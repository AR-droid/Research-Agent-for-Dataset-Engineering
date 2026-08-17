from __future__ import annotations

import uuid
from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import structlog
from starlette.middleware.base import BaseHTTPMiddleware

from ares.domain.exceptions import AresError

logger = structlog.get_logger()

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
        )
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        await logger.ainfo("Request started")
        response = await call_next(request)
        await logger.ainfo("Request completed", status_code=response.status_code)
        return response

def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)
    
    @app.exception_handler(AresError)
    async def ares_error_handler(request: Request, exc: AresError) -> JSONResponse:
        status_code = 400
        if exc.code == "not_found":
            status_code = 404
        elif exc.code == "authentication_error":
            status_code = 401
        elif exc.code == "authorization_error":
            status_code = 403
        elif exc.code == "conflict_error":
            status_code = 409
            
        return JSONResponse(
            status_code=status_code,
            content={"error": exc.message, "code": exc.code}
        )
