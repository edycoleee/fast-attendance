# Backend - FastAPI Attendance System

FastAPI backend untuk sistem attendance RSUD Sulfat.

## 🚀 Setup & Run

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Pastikan PostgreSQL Docker sudah running
cd ../database
docker-compose up -d
cd ../backend

# 3. Run FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Documentation

**Swagger UI**: http://localhost:8000/docs
**ReDoc**: http://localhost:8000/redoc

## 🔌 Database Connection

Backend terhubung ke PostgreSQL Docker:
- Host: `12.50.20.250:5432`
- Database: `attendance_db`
- User: `sultan`
- Password: `Sulfat123#!`

Konfigurasi ada di file [.env](.env)

## 📊 Migrasi Data dari MySQL

Jika ada data di MySQL RSUD Sulfat (192.10.10.15), jalankan script migrasi:

```powershell
# Install library tambahan
pip install mysql-connector-python

# Jalankan migrasi
python migrate.py
```

Script akan otomatis:
- ✓ Koneksi ke MySQL RSUD Sulfat
- ✓ Ambil data dari semua tabel (lokasi, ruang, pegawai, absensi, shift, dll)
- ✓ Insert ke PostgreSQL Docker
- ✓ Reset sequences
- ✓ Total 17 tabel akan dimigrasikan

## 📁 File Structure

```
backend/
├── main.py           # FastAPI app & endpoints
├── database.py       # Database connection
├── models.py         # SQLAlchemy models (17 tables RSUD Sulfat)
├── schemas.py        # Pydantic schemas
├── migrate.py        # MySQL to PostgreSQL migration script
├── requirements.txt  # Dependencies
├── .env             # Environment variables
└── README.md        # This file
```

## 🔧 API Endpoints

### Lokasi
- `POST /lokasi/` - Create lokasi baru
- `GET /lokasi/` - List all lokasi (with pagination)
- `GET /lokasi/{id_lokasi}` - Get lokasi by ID
- `PUT /lokasi/{id_lokasi}` - Update lokasi
- `DELETE /lokasi/{id_lokasi}` - Delete lokasi

### Coming Soon
- Pegawai (Employees)
- Ruang (Departments)
- Absensi (Attendance)
- Shift Management
- User Management

## 🧪 Test API

**Recommended**: Gunakan Swagger UI di http://localhost:8000/docs untuk testing interaktif!

```powershell
# Create lokasi
curl -X POST "http://localhost:8000/lokasi/" -H "Content-Type: application/json" -d '{\"nama_lokasi\":\"RSUD Sulfat\",\"lat\":\"-6.200000\",\"long\":\"106.816666\",\"jarak_area\":100}'

# Get all lokasi
curl http://localhost:8000/lokasi/

# Get lokasi by ID
curl http://localhost:8000/lokasi/1

# Update lokasi
curl -X PUT "http://localhost:8000/lokasi/1" -H "Content-Type: application/json" -d '{\"jarak_area\":150}'

# Delete lokasi
curl -X DELETE "http://localhost:8000/lokasi/1"
```

## 🔍 Troubleshooting

### Error: Can't connect to database
```powershell
# Cek PostgreSQL Docker
cd ../database
docker-compose ps

# Restart jika perlu
docker-compose restart postgres
```

### Error: ModuleNotFoundError
```powershell
# Install ulang dependencies
pip install -r requirements.txt
```

### Error: Port 8000 already in use
```powershell
# Gunakan port lain
uvicorn main:app --reload --port 8001

# Atau kill process yang menggunakan port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```
