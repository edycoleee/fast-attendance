from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


# ============================================================
# RSUD SULFAT MODELS
# ============================================================

class Lokasi(Base):
    __tablename__ = "lokasi"
    
    id_lokasi = Column(Integer, primary_key=True, index=True)
    nama_lokasi = Column(String(255))
    lat = Column(String(255))
    long = Column(String(255))
    jarak_area = Column(Integer)
    
    # Relationship
    absensi = relationship("Absensi", back_populates="lokasi")


class Ruang(Base):
    __tablename__ = "ruang"
    
    id_ruang = Column(Integer, primary_key=True, index=True)
    nama_ruang = Column(String(255))
    status = Column(String(15))
    
    # Relationship
    pegawai = relationship("Pegawai", back_populates="ruang")
    shift_pegawai = relationship("ShiftPegawai", back_populates="ruang")


class Pegawai(Base):
    __tablename__ = "pegawai"
    
    id_pegawai = Column(String(20), primary_key=True, index=True)
    nip = Column(String(255))
    nama = Column(String(255))
    jenis_kelamin = Column(String(255))
    tempat_lahir = Column(String(255))
    tanggal_lahir = Column(Date)
    alamat = Column(Text)
    id_ruang = Column(Integer, ForeignKey("ruang.id_ruang"))
    status = Column(String(15))
    create_at = Column(String(255))
    create_date = Column(DateTime)
    foto = Column(String(100))
    
    # Relationship
    ruang = relationship("Ruang", back_populates="pegawai")
    absensi = relationship("Absensi", back_populates="pegawai")
    detail_shift = relationship("DetailShiftPegawai", back_populates="pegawai")


class Absensi(Base):
    __tablename__ = "absensi"
    
    id_absensi = Column(String(11), primary_key=True, index=True)
    id_lokasi = Column(Integer, ForeignKey("lokasi.id_lokasi"))
    id_pegawai = Column(String(20), ForeignKey("pegawai.id_pegawai"))
    uid = Column(String(30))
    tanggal = Column(DateTime)
    ket = Column(String(50))
    ipaddress = Column(String(20))
    
    # Relationship
    lokasi = relationship("Lokasi", back_populates="absensi")
    pegawai = relationship("Pegawai", back_populates="absensi")


class Shift(Base):
    __tablename__ = "shift"
    
    id_shift = Column(Integer, primary_key=True, index=True)
    nama_shift = Column(String(255))
    jam_masuk = Column(String(255))
    jam_keluar = Column(String(255))


class ShiftPegawai(Base):
    __tablename__ = "shift_pegawai"
    
    id_shift_pegawai = Column(String(20), primary_key=True, index=True)
    tahun = Column(String(255))
    bulan = Column(String(255))
    id_ruang = Column(Integer, ForeignKey("ruang.id_ruang"))
    create_at = Column(String(255))
    create_date = Column(DateTime)
    
    # Relationship
    ruang = relationship("Ruang", back_populates="shift_pegawai")
    detail_shift = relationship("DetailShiftPegawai", back_populates="shift_pegawai")


class DetailShiftPegawai(Base):
    __tablename__ = "detail_shift_pegawai"
    
    id_detail_shift_pegawai = Column(String(20), primary_key=True, index=True)
    id_shift_pegawai = Column(String(20), ForeignKey("shift_pegawai.id_shift_pegawai"))
    id_pegawai = Column(String(20), ForeignKey("pegawai.id_pegawai"))
    hari01 = Column(String(20))
    hari02 = Column(String(20))
    hari03 = Column(String(20))
    hari04 = Column(String(20))
    hari05 = Column(String(20))
    hari06 = Column(String(20))
    hari07 = Column(String(20))
    hari08 = Column(String(20))
    hari09 = Column(String(20))
    hari10 = Column(String(20))
    hari11 = Column(String(20))
    hari12 = Column(String(20))
    hari13 = Column(String(20))
    hari14 = Column(String(20))
    hari15 = Column(String(20))
    hari16 = Column(String(20))
    hari17 = Column(String(20))
    hari18 = Column(String(20))
    hari19 = Column(String(20))
    hari20 = Column(String(20))
    hari21 = Column(String(20))
    hari22 = Column(String(20))
    hari23 = Column(String(20))
    hari24 = Column(String(20))
    hari25 = Column(String(20))
    hari26 = Column(String(20))
    hari27 = Column(String(20))
    hari28 = Column(String(20))
    hari29 = Column(String(20))
    hari30 = Column(String(20))
    hari31 = Column(String(20))
    
    # Relationship
    shift_pegawai = relationship("ShiftPegawai", back_populates="detail_shift")
    pegawai = relationship("Pegawai", back_populates="detail_shift")


# ============================================================
# OLD MODELS (for backward compatibility)
# ============================================================

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    department = Column(String(100))
    position = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    attendances = relationship("Attendance", back_populates="employee")


class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    check_in = Column(DateTime(timezone=True), nullable=False)
    check_out = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="present")  # present, late, absent, leave
    notes = Column(String(500))
    location = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    employee = relationship("Employee", back_populates="attendances")
