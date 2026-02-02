"""
Pydantic schemas untuk API v1
"""
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# ============================================================
# LOKASI SCHEMAS
# ============================================================

class LokasiBase(BaseModel):
    """Base schema untuk Lokasi"""
    nama_lokasi: Optional[str] = None
    lat: Optional[str] = None
    long: Optional[str] = None
    jarak_area: Optional[int] = None


class LokasiCreate(LokasiBase):
    """Schema untuk create lokasi"""
    pass


class LokasiUpdate(BaseModel):
    """Schema untuk update lokasi (semua field optional)"""
    nama_lokasi: Optional[str] = None
    lat: Optional[str] = None
    long: Optional[str] = None
    jarak_area: Optional[int] = None


class LokasiResponse(LokasiBase):
    """Schema untuk response lokasi"""
    id_lokasi: int
    
    class Config:
        from_attributes = True


# ============================================================
# RESPONSE SCHEMAS
# ============================================================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
