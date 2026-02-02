from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import backend.models as models
import backend.schemas as schemas
from backend.database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RSUD Sulfat Attendance System", 
    version="2.0.0",
    description="Sistem Attendance RSUD Sulfat - PostgreSQL"
)

# ============================================================
# LOKASI ENDPOINTS
# ============================================================

@app.post("/lokasi/", response_model=schemas.Lokasi, status_code=status.HTTP_201_CREATED, tags=["Lokasi"])
def create_lokasi(lokasi: schemas.LokasiCreate, db: Session = Depends(get_db)):
    """Create new lokasi"""
    db_lokasi = models.Lokasi(**lokasi.model_dump())
    db.add(db_lokasi)
    db.commit()
    db.refresh(db_lokasi)
    return db_lokasi


@app.get("/lokasi/", response_model=List[schemas.Lokasi], tags=["Lokasi"])
def get_all_lokasi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all lokasi"""
    lokasi = db.query(models.Lokasi).offset(skip).limit(limit).all()
    return lokasi


@app.get("/lokasi/{id_lokasi}", response_model=schemas.Lokasi, tags=["Lokasi"])
def get_lokasi_by_id(id_lokasi: int, db: Session = Depends(get_db)):
    """Get lokasi by ID"""
    lokasi = db.query(models.Lokasi).filter(models.Lokasi.id_lokasi == id_lokasi).first()
    if lokasi is None:
        raise HTTPException(status_code=404, detail="Lokasi not found")
    return lokasi


@app.put("/lokasi/{id_lokasi}", response_model=schemas.Lokasi, tags=["Lokasi"])
def update_lokasi(
    id_lokasi: int, 
    lokasi_update: schemas.LokasiUpdate, 
    db: Session = Depends(get_db)
):
    """Update lokasi"""
    db_lokasi = db.query(models.Lokasi).filter(models.Lokasi.id_lokasi == id_lokasi).first()
    if db_lokasi is None:
        raise HTTPException(status_code=404, detail="Lokasi not found")
    
    update_data = lokasi_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_lokasi, field, value)
    
    db.commit()
    db.refresh(db_lokasi)
    return db_lokasi


@app.delete("/lokasi/{id_lokasi}", status_code=status.HTTP_204_NO_CONTENT, tags=["Lokasi"])
def delete_lokasi(id_lokasi: int, db: Session = Depends(get_db)):
    """Delete lokasi"""
    db_lokasi = db.query(models.Lokasi).filter(models.Lokasi.id_lokasi == id_lokasi).first()
    if db_lokasi is None:
        raise HTTPException(status_code=404, detail="Lokasi not found")
    
    db.delete(db_lokasi)
    db.commit()
    return None


@app.get("/", tags=["Root"])
def root():
    """Root endpoint"""
    return {
        "message": "RSUD Sulfat Attendance System API",
        "version": "2.0.0",
        "database": "PostgreSQL",
        "docs": "/docs",
        "endpoints": {
            "lokasi": "/lokasi"
        }
    }
