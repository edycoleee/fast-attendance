from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

# ============================================================
# LOKASI SCHEMAS
# ============================================================

class LokasiBase(BaseModel):
    nama_lokasi: Optional[str] = None
    lat: Optional[str] = None
    long: Optional[str] = None
    jarak_area: Optional[int] = None

class LokasiCreate(LokasiBase):
    pass

class LokasiUpdate(BaseModel):
    nama_lokasi: Optional[str] = None
    lat: Optional[str] = None
    long: Optional[str] = None
    jarak_area: Optional[int] = None

class Lokasi(LokasiBase):
    id_lokasi: int
    
    class Config:
        from_attributes = True


# ============================================================
# OLD EMPLOYEE SCHEMAS (for backward compatibility)
# ============================================================

class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    department: Optional[str] = None
    position: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None

class Employee(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Attendance Schemas
class AttendanceBase(BaseModel):
    employee_id: int
    check_in: datetime
    check_out: Optional[datetime] = None
    status: str = "present"
    notes: Optional[str] = None
    location: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    check_out: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    location: Optional[str] = None

class Attendance(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
