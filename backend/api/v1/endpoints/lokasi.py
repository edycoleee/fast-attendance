"""
Lokasi API endpoints
"""
from fastapi import APIRouter, status, Query
from typing import List

from api.v1.schemas import (
    LokasiCreate,
    LokasiUpdate,
    LokasiResponse,
    MessageResponse
)
from services.lokasi_service import LokasiService
from utils.response import success_response, paginated_response
from utils.logger import get_logger

router = APIRouter(prefix="/lokasi", tags=["Lokasi"])
lokasi_service = LokasiService()
logger = get_logger(__name__)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create Lokasi Baru"
)
def create_lokasi(lokasi: LokasiCreate):
    """
    Create lokasi baru.
    
    - **nama_lokasi**: Nama lokasi
    - **lat**: Latitude
    - **long**: Longitude
    - **jarak_area**: Jarak area dalam meter
    """
    logger.info(f"Creating new lokasi: {lokasi.nama_lokasi}")
    data = lokasi.model_dump()
    result = lokasi_service.create_lokasi(data)
    logger.info(f"Lokasi created successfully with ID: {result.get('id_lokasi')}")
    
    return success_response(
        message="Lokasi berhasil dibuat",
        data=result
    )


@router.get(
    "/",
    summary="Get All Lokasi"
)
def get_all_lokasi(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records")
):
    """
    Get semua lokasi dengan pagination.
    
    - **skip**: Offset untuk pagination (default: 0)
    - **limit**: Maximum records (default: 100, max: 100)
    """
    logger.info(f"Fetching lokasi list: skip={skip}, limit={limit}")
    
    # Get data
    data = lokasi_service.get_all_lokasi(skip=skip, limit=limit)
    
    # Get total count
    total = lokasi_service.get_lokasi_count()
    
    # Calculate page number
    page = (skip // limit) + 1 if limit > 0 else 1
    
    logger.info(f"Retrieved {len(data)} lokasi records")
    
    return paginated_response(
        message="Lokasi berhasil diambil",
        data=data,
        page=page,
        limit=limit,
        total=total
    )


@router.get(
    "/search",
    summary="Search Lokasi by Nama"
)
def search_lokasi(
    name: str = Query(..., min_length=1, description="Nama lokasi untuk dicari")
):
    """
    Search lokasi berdasarkan nama (partial match).
    
    - **name**: Nama lokasi (case-insensitive)
    """
    logger.info(f"Searching lokasi with name: {name}")
    data = lokasi_service.search_lokasi(name)
    logger.info(f"Found {len(data)} lokasi matching '{name}'")
    
    return success_response(
        message=f"Ditemukan {len(data)} lokasi",
        data=data
    )


@router.get(
    "/count",
    summary="Get Total Lokasi Count"
)
def get_lokasi_count():
    """Get total jumlah lokasi."""
    logger.info("Fetching lokasi count")
    count = lokasi_service.get_lokasi_count()
    logger.info(f"Total lokasi: {count}")
    
    return success_response(
        message="Total lokasi berhasil diambil",
        data={"total": count}
    )


@router.get(
    "/{id_lokasi}",
    summary="Get Lokasi by ID"
)
def get_lokasi_by_id(id_lokasi: int):
    """
    Get lokasi berdasarkan ID.
    
    - **id_lokasi**: ID lokasi
    """
    logger.info(f"Fetching lokasi with ID: {id_lokasi}")
    result = lokasi_service.get_lokasi_by_id(id_lokasi)
    logger.info(f"Lokasi found: {result.get('nama_lokasi')}")
    
    return success_response(
        message="Lokasi berhasil diambil",
        data=result
    )


@router.put(
    "/{id_lokasi}",
    summary="Update Lokasi"
)
def update_lokasi(id_lokasi: int, lokasi_update: LokasiUpdate):
    """
    Update lokasi.
    
    - **id_lokasi**: ID lokasi yang akan diupdate
    - Semua field optional, hanya field yang diisi yang akan diupdate
    """
    logger.info(f"Updating lokasi ID: {id_lokasi}")
    data = lokasi_update.model_dump(exclude_unset=True)
    result = lokasi_service.update_lokasi(id_lokasi, data)
    logger.info(f"Lokasi updated successfully: {result.get('nama_lokasi')}")
    
    return success_response(
        message="Lokasi berhasil diupdate",
        data=result
    )


@router.delete(
    "/{id_lokasi}",
    status_code=status.HTTP_200_OK,
    summary="Delete Lokasi"
)
def delete_lokasi(id_lokasi: int):
    """
    Delete lokasi.
    
    - **id_lokasi**: ID lokasi yang akan dihapus
    """
    logger.info(f"Deleting lokasi ID: {id_lokasi}")
    lokasi_service.delete_lokasi(id_lokasi)
    logger.info(f"Lokasi deleted successfully: ID {id_lokasi}")
    
    return success_response(
        message="Lokasi berhasil dihapus",
        data={"id_lokasi": id_lokasi}
    )
