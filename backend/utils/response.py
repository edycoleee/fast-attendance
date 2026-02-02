"""
Standard response utilities untuk FastAPI
"""
from typing import Any, Optional, Dict
from pydantic import BaseModel


class StandardResponse(BaseModel):
    """Standard response model"""
    success: bool
    message: str
    data: Optional[Any] = None


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    page: int
    limit: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel):
    """Paginated response model"""
    success: bool
    message: str
    data: list
    meta: PaginationMeta


def success_response(
    message: str = "Success",
    data: Any = None,
    status_code: int = 200
) -> Dict[str, Any]:
    """
    Create standard success response
    
    Args:
        message: Success message
        data: Response data
        status_code: HTTP status code (not used, for compatibility)
    
    Returns:
        Dictionary with success response format
    
    Example:
        return success_response("Lokasi created", data=lokasi_data)
    """
    return {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }


def error_response(
    message: str = "Error",
    data: Any = None,
    status_code: int = 400
) -> Dict[str, Any]:
    """
    Create standard error response
    
    Args:
        message: Error message
        data: Additional error data
        status_code: HTTP status code (not used, for compatibility)
    
    Returns:
        Dictionary with error response format
    
    Example:
        return error_response("Validation failed", data={"field": "error"})
    """
    return {
        "success": False,
        "message": message,
        "data": data if data is not None else {}
    }


def paginated_response(
    message: str = "Success",
    data: list = None,
    page: int = 1,
    limit: int = 10,
    total: int = 0
) -> Dict[str, Any]:
    """
    Create paginated response
    
    Args:
        message: Success message
        data: List of items
        page: Current page
        limit: Items per page
        total: Total items count
    
    Returns:
        Dictionary with paginated response format
    
    Example:
        return paginated_response(
            "Lokasi retrieved",
            data=lokasi_list,
            page=1,
            limit=10,
            total=50
        )
    """
    total_pages = (total + limit - 1) // limit if limit > 0 else 0
    
    return {
        "success": True,
        "message": message,
        "data": data if data is not None else [],
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages
        }
    }
