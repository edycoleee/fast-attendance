"""
Middleware untuk logging requests di FastAPI
"""
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware untuk log semua HTTP requests
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Log request dan response
        
        Args:
            request: FastAPI request object
            call_next: Next middleware/route handler
        
        Returns:
            Response object
        """
        # Start timer
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate process time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Time: {process_time:.3f}s"
            )
            
            # Add process time to response headers
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                f"Error: {request.method} {request.url.path} "
                f"Error: {str(e)} "
                f"Time: {process_time:.3f}s",
                exc_info=True
            )
            raise
