
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn
from contextlib import asynccontextmanager

from infrastructure.web.controllers import (
    book_controller,
    user_controller,
    library_controller,
    auth_controller,
    author_controller
)
from domain.models.exceptions.resource import (
    ResourceConflictError,
    ResourceNotFoundError,
    ResourceUnauthorizedError,
    InvalidUserTypeException
)
from domain.models.exceptions.business_exception import BusinessError
from infrastructure.middleware.security_logging import SecurityLoggingMiddleware


# 🔒 SECURITY: Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting application on port 8009")
    yield
    print(f"Stopping application on port 8009")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Library Management System API",
        description="API for managing a library system with books, users, and loans",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # 🔒 SECURITY: Add rate limiter to app state
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # 🔒 SECURITY: Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Update with your frontend URL
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    
    # 🔒 SECURITY: Add security logging middleware
    app.add_middleware(SecurityLoggingMiddleware)
    
    # Register routers
    app.include_router(book_controller.router, prefix="/books")
    app.include_router(library_controller.router, prefix="/library/books")
    app.include_router(user_controller.router, prefix="/users")
    app.include_router(auth_controller.router, prefix="/auth")
    app.include_router(author_controller.router, prefix="/authors")
    
    # Register exception handlers
    @app.exception_handler(BusinessError)
    async def business_exception_handler(request: Request, exc: BusinessError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)}
        )

    @app.exception_handler(ResourceConflictError)
    async def book_already_exists_exception_handler(request: Request, exc: ResourceConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)}
        )
        
    @app.exception_handler(ResourceNotFoundError)
    async def book_not_found_exception_handler(request: Request, exc: ResourceNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)}
        )

    @app.exception_handler(ResourceUnauthorizedError)
    async def unauthorized_exception_handler(request: Request, exc: ResourceUnauthorizedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)}
        )
        
    @app.exception_handler(InvalidUserTypeException)
    async def invalid_user_type_exception(request: Request, exc: InvalidUserTypeException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)}
        )
        
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        # 🔒 SECURITY: Log detailed error internally
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unhandled exception: {type(exc).__name__} - {str(exc)}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
        
    return app


app = create_app()


# If the script is executed directly, start the server
if __name__ == "__main__":
    uvicorn.run("main:app", port=8009, reload=True)