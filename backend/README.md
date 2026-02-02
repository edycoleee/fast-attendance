# Backend - FastAPI Attendance System

FastAPI backend untuk sistem attendance RSUD Sulfat dengan **Clean Architecture**.

## 📚 Dokumentasi

- **[Quick Start Guide](QUICK_START.md)** - Cara cepat memulai development
- **[Refactoring Summary](REFACTORING_SUMMARY.md)** - Detail perubahan refactoring
- **[Architecture Diagram](ARCHITECTURE_DIAGRAM.md)** - Visualisasi clean architecture
- **[Utils README](utils/README.md)** - Database utilities documentation

## 🏗️ Clean Architecture Structure

```
backend/
├── api/                          # API Layer (Presentation)
│   └── v1/
│       ├── endpoints/            # Route handlers
│       │   └── lokasi.py
│       ├── router.py             # API v1 router
│       └── schemas.py            # Pydantic schemas
│
├── services/                     # Business Logic Layer
│   └── lokasi_service.py         # Business rules & validations
│
├── repositories/                 # Data Access Layer
│   └── lokasi_repository.py      # Raw SQL queries (psycopg2)
│
├── config/                       # Configuration
│   ├── settings.py               # Environment settings
│   └── database.py               # Database connections
│
├── utils/                        # Utilities
│   ├── db.py                     # Database helpers
│   └── README.md
│
├── models.py                     # SQLAlchemy models (legacy/optional)
├── schemas.py                    # Legacy schemas (moved to api/v1/)
├── database.py                   # Legacy database (moved to config/)
├── main.py                       # FastAPI app entry point
├── requirements.txt              # Dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## 📐 Architecture Layers

### 1. **API Layer** (`api/v1/`)
- **Endpoints**: Route handlers yang menerima HTTP requests
- **Schemas**: Pydantic models untuk request/response validation
- **Router**: Menggabungkan semua endpoints

### 2. **Service Layer** (`services/`)
- **Business Logic**: Aturan bisnis, validasi, dan koordinasi
- **Error Handling**: Menangani exceptions dengan HTTPException
- **Independent**: Tidak bergantung pada framework tertentu

### 3. **Repository Layer** (`repositories/`)
- **Data Access**: Raw SQL queries menggunakan psycopg2
- **Database Operations**: CRUD operations dengan SQL murni
- **Query Optimization**: Optimasi query untuk performa

### 4. **Config Layer** (`config/`)
- **Settings**: Centralized configuration dari environment
- **Database**: Database connection management


## 🚀 Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup .env file (sudah ada template)
cp .env.example .env  # Jika belum ada

# 3. Pastikan PostgreSQL Docker running
cd ../database
docker-compose up -d
cd ../backend

# 4. Run FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔌 Database Connection

Backend menggunakan **dual database approach**:

### 1. **psycopg2** (Raw SQL - Primary)
Digunakan untuk Clean Architecture dengan raw SQL queries:
```python
from backend.repositories.lokasi_repository import LokasiRepository

repo = LokasiRepository()
lokasi = repo.find_all()
```

### 2. **SQLAlchemy** (ORM - Optional)
Tersedia untuk backward compatibility:
```python
from backend.database import get_db
from backend.models import Lokasi
```

**Database Config** (dari `.env`):
- Host: `12.50.20.250:5432`
- Database: `attendance_db`
- User: `sultan`
- Password: `Sulfat123#!`


## 📡 API Documentation

**Base URL**: `http://localhost:8000`

**Swagger UI**: http://localhost:8000/docs  
**ReDoc**: http://localhost:8000/redoc  
**OpenAPI**: http://localhost:8000/openapi.json

## 🔧 API Endpoints (v1)

### Lokasi API (`/api/v1/lokasi`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/lokasi/` | Create lokasi baru |
| GET | `/api/v1/lokasi/` | List all lokasi (pagination) |
| GET | `/api/v1/lokasi/search?name=` | Search lokasi by nama |
| GET | `/api/v1/lokasi/count` | Get total count lokasi |
| GET | `/api/v1/lokasi/{id}` | Get lokasi by ID |
| PUT | `/api/v1/lokasi/{id}` | Update lokasi |
| DELETE | `/api/v1/lokasi/{id}` | Delete lokasi |

### Root Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |


## 🧪 Testing API

### Using Swagger UI (Recommended)
Buka http://localhost:8000/docs untuk testing interaktif!

### Using cURL

```bash
# Create lokasi
curl -X POST "http://localhost:8000/api/v1/lokasi/" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_lokasi": "RSUD Sulfat",
    "lat": "-6.200000",
    "long": "106.816666",
    "jarak_area": 100
  }'

# Get all lokasi
curl http://localhost:8000/api/v1/lokasi/

# Search lokasi
curl "http://localhost:8000/api/v1/lokasi/search?name=sulfat"

# Get count
curl http://localhost:8000/api/v1/lokasi/count

# Get by ID
curl http://localhost:8000/api/v1/lokasi/1

# Update lokasi
curl -X PUT "http://localhost:8000/api/v1/lokasi/1" \
  -H "Content-Type: application/json" \
  -d '{"jarak_area": 150}'

# Delete lokasi
curl -X DELETE http://localhost:8000/api/v1/lokasi/1
```

## 💻 Development Guide

### Adding New Endpoint (Example: Pegawai)

#### 1. Create Repository (`repositories/pegawai_repository.py`)
```python
from backend.config.database import get_db_connection, get_db_cursor

class PegawaiRepository:
    @staticmethod
    def find_all():
        query = "SELECT * FROM pegawai"
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
```

#### 2. Create Service (`services/pegawai_service.py`)
```python
from backend.repositories.pegawai_repository import PegawaiRepository

class PegawaiService:
    def __init__(self):
        self.repository = PegawaiRepository()
    
    def get_all_pegawai(self):
        return self.repository.find_all()
```

#### 3. Create Endpoint (`api/v1/endpoints/pegawai.py`)
```python
from fastapi import APIRouter
from backend.services.pegawai_service import PegawaiService

router = APIRouter(prefix="/pegawai", tags=["Pegawai"])
service = PegawaiService()

@router.get("/")
def get_all_pegawai():
    return service.get_all_pegawai()
```

#### 4. Register Router (`api/v1/router.py`)
```python
from backend.api.v1.endpoints import lokasi, pegawai

api_router.include_router(lokasi.router)
api_router.include_router(pegawai.router)  # Add this
```

## 📦 Dependencies

```
fastapi==0.109.0              # Web framework
uvicorn==0.27.0               # ASGI server
sqlalchemy==2.0.25            # ORM (optional)
psycopg2-binary==2.9.9        # PostgreSQL adapter
python-dotenv==1.0.0          # Environment variables
pydantic==2.5.3               # Data validation
pydantic-settings==2.1.0      # Settings management
```

## 🔐 Environment Variables

File `.env`:
```env
# Database
POSTGRES_DB=attendance_db
POSTGRES_USER=sultan
POSTGRES_PASSWORD=Sulfat123#!
POSTGRES_HOST=12.50.20.250
POSTGRES_PORT=5432

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
PGADMIN_PORT=5050
```

## 🎯 Benefits of Clean Architecture

✅ **Separation of Concerns**: Setiap layer punya tanggung jawab jelas  
✅ **Testability**: Mudah di-test karena independent  
✅ **Maintainability**: Mudah di-maintain dan extend  
✅ **Scalability**: Mudah di-scale saat aplikasi berkembang  
✅ **Raw SQL**: Full control atas query dengan psycopg2  
✅ **Type Safety**: Pydantic untuk validasi request/response  

## 🔄 Migration from Old Structure

### Before (Monolithic)
```python
# main.py - Everything in one file
@app.get("/lokasi/")
def get_lokasi(db: Session = Depends(get_db)):
    return db.query(Lokasi).all()
```

### After (Clean Architecture)
```python
# Repository (Data Access)
class LokasiRepository:
    def find_all(self):
        query = "SELECT * FROM lokasi"
        # ... SQL execution

# Service (Business Logic)
class LokasiService:
    def get_all_lokasi(self):
        return self.repository.find_all()

# Endpoint (API Handler)
@router.get("/")
def get_all_lokasi():
    return service.get_all_lokasi()
```

## 📊 Next Features to Implement

- [ ] Pegawai (Employees) endpoints
- [ ] Ruang (Departments) endpoints
- [ ] Absensi (Attendance) endpoints
- [ ] Shift Management endpoints
- [ ] User Authentication & Authorization
- [ ] File Upload (Foto pegawai)
- [ ] Reporting & Analytics
- [ ] Face Recognition Integration

## 🐛 Troubleshooting

### Error: Module not found
```bash
# Make sure you're in backend directory
cd backend
python -m pip install -r requirements.txt
```

### Database connection error
```bash
# Check if PostgreSQL is running
cd database
docker-compose ps

# Restart if needed
docker-compose restart
```

### Import errors
```bash
# Run from backend directory
uvicorn main:app --reload

# Or from root
uvicorn backend.main:app --reload
```

## 📝 License

RSUD Sulfat Internal Project

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
