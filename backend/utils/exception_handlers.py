"""
Exception handlers untuk FastAPI
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.logger import logger
from utils.response import error_response


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions
    
    Args:
        request: FastAPI request
        exc: HTTP exception
    
    Returns:
        JSONResponse with error details
    """
    logger.warning(
        f"HTTP Exception: {exc.status_code} - {exc.detail} "
        f"Path: {request.url.path}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.detail,
            status_code=exc.status_code
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors from Pydantic
    
    Args:
        request: FastAPI request
        exc: Validation error
    
    Returns:
        JSONResponse with validation error details
    """
    errors = exc.errors()
    
    logger.warning(
        f"Validation Error: {request.url.path} "
        f"Errors: {errors}"
    )
    
    # Format validation errors
    formatted_errors = []
    for error in errors:
        formatted_errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="Validation error",
            data={"errors": formatted_errors},
            status_code=422
        )
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all unhandled exceptions
    
    Args:
        request: FastAPI request
        exc: Exception
    
    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"Unhandled Exception: {request.url.path} "
        f"Error: {str(exc)}",
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            message="Internal server error",
            data={"error": str(exc)},
            status_code=500
        )
    )
