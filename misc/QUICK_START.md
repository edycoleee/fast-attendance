# 🚀 Quick Start Guide - Clean Architecture

## Prerequisites

- Python 3.11+
- PostgreSQL (via Docker)
- Virtual environment activated

## 📥 Installation

```bash
# 1. Masuk ke directory backend
cd /home/sultan/fast/fast-attendance/backend

# 2. Install dependencies
pip install -r requirements.txt
```

## 🗄️ Database Setup

```bash
# 1. Masuk ke directory database
cd /home/sultan/fast/fast-attendance/database

# 2. Start PostgreSQL dengan Docker
docker-compose up -d

# 3. Verify database running
docker-compose ps

# Expected output:
# attendance-db-postgres   Up   5432/tcp
# attendance-db-pgadmin    Up   80/tcp
```

## 🏃 Running the Server

```bash
# 1. Kembali ke backend directory
cd /home/sultan/fast/fast-attendance/backend

# 2. Run FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Server akan berjalan di: http://localhost:8000
```

## 📖 API Documentation

Setelah server running, akses:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing the API

### 1. Via Swagger UI (Recommended)

1. Buka http://localhost:8000/docs
2. Expand endpoint yang ingin di-test
3. Click "Try it out"
4. Isi parameter/body
5. Click "Execute"

### 2. Via cURL

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

### 3. Via Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Create lokasi
response = requests.post(
    f"{BASE_URL}/lokasi/",
    json={
        "nama_lokasi": "RSUD Sulfat",
        "lat": "-6.200000",
        "long": "106.816666",
        "jarak_area": 100
    }
)
print(response.json())

# Get all lokasi
response = requests.get(f"{BASE_URL}/lokasi/")
print(response.json())
```

## 🛠️ Development

### Adding New Endpoint

Ikuti pattern Clean Architecture:

#### Step 1: Create Repository
```python
# repositories/pegawai_repository.py
from config.database import get_db_connection, get_db_cursor

class PegawaiRepository:
    @staticmethod
    def find_all():
        query = "SELECT * FROM pegawai ORDER BY nama"
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def find_by_id(id_pegawai: str):
        query = "SELECT * FROM pegawai WHERE id_pegawai = %(id)s"
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query, {'id': id_pegawai})
            result = cursor.fetchone()
            return dict(result) if result else None
```

#### Step 2: Create Service
```python
# services/pegawai_service.py
from repositories.pegawai_repository import PegawaiRepository
from fastapi import HTTPException, status

class PegawaiService:
    def __init__(self):
        self.repository = PegawaiRepository()
    
    def get_all_pegawai(self):
        try:
            return self.repository.find_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error: {str(e)}"
            )
    
    def get_pegawai_by_id(self, id_pegawai: str):
        result = self.repository.find_by_id(id_pegawai)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pegawai {id_pegawai} not found"
            )
        return result
```

#### Step 3: Create Schemas (if needed)
```python
# api/v1/schemas.py
class PegawaiBase(BaseModel):
    id_pegawai: str
    nama: str
    nip: Optional[str] = None

class PegawaiResponse(PegawaiBase):
    class Config:
        from_attributes = True
```

#### Step 4: Create Endpoint
```python
# api/v1/endpoints/pegawai.py
from fastapi import APIRouter
from typing import List
from api.v1.schemas import PegawaiResponse
from services.pegawai_service import PegawaiService

router = APIRouter(prefix="/pegawai", tags=["Pegawai"])
service = PegawaiService()

@router.get("/", response_model=List[PegawaiResponse])
def get_all_pegawai():
    """Get all pegawai"""
    return service.get_all_pegawai()

@router.get("/{id_pegawai}", response_model=PegawaiResponse)
def get_pegawai(id_pegawai: str):
    """Get pegawai by ID"""
    return service.get_pegawai_by_id(id_pegawai)
```

#### Step 5: Register Router
```python
# api/v1/router.py
from fastapi import APIRouter
from api.v1.endpoints import lokasi, pegawai  # Add pegawai

api_router = APIRouter()
api_router.include_router(lokasi.router)
api_router.include_router(pegawai.router)  # Add this line
```

### Testing Architecture

```bash
# Run architecture validation
python test_architecture.py

# Expected output:
# ✓ All imports successful!
# ✓ Clean architecture structure verified!
# 🎉 All tests passed!
```

## 📊 Database Access

### Using Repository (Recommended)
```python
from repositories.lokasi_repository import LokasiRepository

# Get all
lokasi_list = LokasiRepository.find_all()

# Get by ID
lokasi = LokasiRepository.find_by_id(1)

# Create
new_lokasi = LokasiRepository.create({
    'nama_lokasi': 'Test',
    'lat': '-6.2',
    'long': '106.8',
    'jarak_area': 100
})

# Update
updated = LokasiRepository.update(1, {
    'jarak_area': 150
})

# Delete
success = LokasiRepository.delete(1)
```

### Using Utils (Alternative)
```python
from utils.db import execute_query, execute_update

# Select
rows = execute_query("SELECT * FROM lokasi")

# Select one
row = execute_query(
    "SELECT * FROM lokasi WHERE id_lokasi = %s",
    (1,),
    fetch_one=True
)

# Insert
execute_update(
    "INSERT INTO lokasi (nama_lokasi) VALUES (%s)",
    ("Test",)
)
```

## 🔧 Configuration

### Environment Variables (.env)
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

### Accessing Settings in Code
```python
from config.settings import settings

print(settings.APP_NAME)
print(settings.DATABASE_URL)
print(settings.DB_CONFIG)
```

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port is already in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### Database connection error
```bash
# Check if PostgreSQL is running
cd database
docker-compose ps

# Check logs
docker-compose logs postgres

# Restart database
docker-compose restart
```

### Import errors
```bash
# Make sure you're in backend directory
cd /home/sultan/fast/fast-attendance/backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Module not found
```bash
# Run from backend directory
cd /home/sultan/fast/fast-attendance/backend
uvicorn main:app --reload
```

## 📚 Resources

- **README.md**: General documentation
- **REFACTORING_SUMMARY.md**: Refactoring details
- **ARCHITECTURE_DIAGRAM.md**: Architecture visualization
- **utils/README.md**: Database utilities guide

## 🎯 Next Steps

1. ✅ Test current endpoints di Swagger UI
2. ⬜ Add Pegawai endpoints
3. ⬜ Add Ruang endpoints
4. ⬜ Add Absensi endpoints
5. ⬜ Add Authentication
6. ⬜ Add File Upload
7. ⬜ Add Face Recognition

---

**Happy Coding! 🚀**
