"""
API Router untuk v1
"""
from fastapi import APIRouter
from api.v1.endpoints import lokasi

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(lokasi.router)

# Add more routers here as they are created
# api_router.include_router(pegawai.router)
# api_router.include_router(ruang.router)
# api_router.include_router(absensi.router)
