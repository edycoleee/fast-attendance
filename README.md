# RSUD Sulfat - Fast Attendance System

Sistem attendance dengan PostgreSQL (Docker) untuk RSUD Sulfat.

## 📁 Project Structure

```
fast-attendance/
├── .env                    # Environment configuration (EDIT THIS!)
├── .env.example            # Template untuk komputer baru
├── README.md               # This file
├── CHEATSHEET.md           # Quick reference
├── DOCKER_ENV_VARS.md      # Docker variables guide
├── ENV_SETUP.md            # Complete setup guide
│
├── backend/                # FastAPI Backend (Clean Architecture)
│   ├── main.py             # FastAPI app entry point
│   ├── requirements.txt    # Python dependencies
│   │
│   ├── config/             # Configuration layer
│   │   ├── settings.py     # Pydantic settings (from .env)
│   │   └── database.py     # Database connections
│   │
│   ├── api/                # API/Presentation layer
│   │   └── v1/
│   │       ├── router.py   # Main API router
│   │       ├── schemas.py  # Request/Response models
│   │       └── endpoints/
│   │           └── lokasi.py  # Lokasi endpoints
│   │
│   ├── services/           # Business logic layer
│   │   └── lokasi_service.py
│   │
│   ├── repositories/       # Data access layer (Raw SQL)
│   │   └── lokasi_repository.py
│   │
│   ├── utils/              # Utilities
│   │   ├── response.py     # Standard response format
│   │   ├── logger.py       # Logging configuration
│   │   ├── middleware.py   # Request logging middleware
│   │   ├── exception_handlers.py  # Global exception handlers
│   │   └── db.py           # Database utilities (psycopg2)
│   │
│   └── logs/               # Application logs
│       └── app_YYYYMMDD.log
│
├── database/               # PostgreSQL Docker
│   ├── docker-compose.yml  # Auto-load from ../.env
│   ├── init.sql            # Database schema & seed data
│   └── README.md
│
└── frontend/               # React/Vue (coming soon)
```

## 🚀 Quick Start

### 1️⃣ Konfigurasi Environment (PENTING!)

**Edit `.env` sesuai IP komputer Anda:**

```bash
nano .env
```

**Yang perlu diganti:**
```env
# IP untuk Docker binding (biasanya 0.0.0.0 untuk akses dari mana saja)
DOCKER_HOST_IP=0.0.0.0

# IP komputer yang menjalankan Docker
POSTGRES_HOST=192.168.30.14  # ← GANTI SESUAI IP ANDA!
```

**Cek IP komputer:**
```bash
ifconfig  # atau ip addr show
```

### 2️⃣ Start Database (PostgreSQL dengan Docker)

```bash
cd database
docker compose up -d

# Cek status (tunggu sampai "healthy")
docker compose ps
```

**Akses Database:**
- PostgreSQL: `192.168.30.14:5432` (sesuai IP Anda)
- pgAdmin: http://192.168.30.14:5050
  - Email: `admin@admin.com`
  - Password: `admin`

### 3️⃣ Setup Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Atau gunakan virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Dependencies yang diinstall:**
- FastAPI 0.109.0 - Web framework
- psycopg2-binary 2.9.9 - PostgreSQL driver (raw SQL)
- pydantic-settings 2.1.0 - Settings management
- uvicorn 0.27.0 - ASGI server

### 4️⃣ Run Backend

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Akses:**
- **API Documentation (Swagger)**: http://192.168.30.14:8000/docs
- **Alternative Docs (ReDoc)**: http://192.168.30.14:8000/redoc
- **Health Check**: http://192.168.30.14:8000/

### 🛑 Stop Backend

```bash
# Ctrl+C di terminal yang menjalankan uvicorn

# Atau kill process
pkill -f "uvicorn main:app"
```

### 🔄 Restart Backend (Setelah Edit .env)

```bash
pkill -f "uvicorn main:app"
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


## 📊 Database Schema

### Tables Overview

```sql
-- 1. lokasi (Location Management)
CREATE TABLE lokasi (
    id_lokasi SERIAL PRIMARY KEY,
    nama_lokasi VARCHAR(255),    -- Nama lokasi (RSUD Sulfat, dll)
    lat VARCHAR(255),             -- Latitude GPS
    long VARCHAR(255),            -- Longitude GPS  
    jarak_area INTEGER            -- Radius area check-in (meter)
);

-- 2. ruang (Room/Department Management)
CREATE TABLE ruang (
    id_ruang SERIAL PRIMARY KEY,
    nama_ruang VARCHAR(255),     -- Nama ruangan
    status VARCHAR(15)           -- Status: active/inactive
);

-- 3. pegawai (Employee Management)
CREATE TABLE pegawai (
    id_pegawai VARCHAR(20) PRIMARY KEY,
    nip VARCHAR(255),            -- NIP pegawai
    nama VARCHAR(255),           -- Nama lengkap
    jenis_kelamin VARCHAR(255),  -- L/P
    tempat_lahir VARCHAR(255),
    tanggal_lahir DATE,
    alamat TEXT,
    id_ruang INTEGER,            -- FK ke ruang
    status VARCHAR(15),          -- active/inactive
    foto VARCHAR(100),           -- Path foto profil
    create_date TIMESTAMP,
    FOREIGN KEY (id_ruang) REFERENCES ruang(id_ruang)
);

-- 4. absensi (Attendance Records)
CREATE TABLE absensi (
    id_absensi VARCHAR(11) PRIMARY KEY,
    id_lokasi INTEGER,           -- FK ke lokasi
    id_pegawai VARCHAR(20),      -- FK ke pegawai
    uid VARCHAR(30),             -- Face recognition UID
    tanggal TIMESTAMP,           -- Waktu check-in/out
    ket VARCHAR(50),             -- Keterangan: masuk/pulang
    ipaddress VARCHAR(20),       -- IP device
    FOREIGN KEY (id_lokasi) REFERENCES lokasi(id_lokasi),
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai)
);

-- 5. shift (Shift Templates)
CREATE TABLE shift (
    id_shift SERIAL PRIMARY KEY,
    nama_shift VARCHAR(255),     -- Nama shift (Pagi/Siang/Malam)
    jam_masuk VARCHAR(255),      -- Jam mulai shift
    jam_keluar VARCHAR(255)      -- Jam selesai shift
);
```

**Extensions:**
- `vector` - untuk face recognition embeddings (pgvector)

**Sample Data:**
```sql
-- Lokasi default
INSERT INTO lokasi VALUES (1, 'RSUD Sulfat', '-6.200000', '106.816666', 100);
```


## 🔧 API Endpoints

### 📍 Lokasi Management (`/api/v1/lokasi`)

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|-------------|
| `POST` | `/api/v1/lokasi/` | Create lokasi baru | `{"nama_lokasi": str, "lat": str, "long": str, "jarak_area": int}` |
| `GET` | `/api/v1/lokasi/` | Get all lokasi (paginated) | Query: `skip=0&limit=100` |
| `GET` | `/api/v1/lokasi/{id}` | Get lokasi by ID | - |
| `PUT` | `/api/v1/lokasi/{id}` | Update lokasi | `{"nama_lokasi": str, "lat": str, "long": str, "jarak_area": int}` |
| `DELETE` | `/api/v1/lokasi/{id}` | Delete lokasi | - |
| `GET` | `/api/v1/lokasi/count` | Count total lokasi | - |
| `GET` | `/api/v1/lokasi/search` | Search by nama_lokasi | Query: `q=keyword` |

### 📋 Response Format

**Success Response:**
```json
{
  "success": true,
  "message": "Lokasi berhasil dibuat",
  "data": {
    "id_lokasi": 1,
    "nama_lokasi": "RSUD Sulfat",
    "lat": "-6.200000",
    "long": "106.816666",
    "jarak_area": 100
  }
}
```

**Paginated Response:**
```json
{
  "success": true,
  "message": "Lokasi berhasil diambil",
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 100,
    "total": 5,
    "total_pages": 1
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error message",
  "data": null
}
```

### 🚧 Coming Soon
- `/api/v1/pegawai` - Employee management
- `/api/v1/ruang` - Room management  
- `/api/v1/absensi` - Attendance records
- `/api/v1/shift` - Shift management

## 🛠️ Development Commands

### Docker Database Management

```bash
# Stop database
cd database
docker compose down

# View logs
docker compose logs -f postgres

# Restart containers
docker compose restart

# Reset database (HAPUS SEMUA DATA!)
docker compose down -v
docker compose up -d

# Check container status
docker compose ps

# Enter PostgreSQL shell
docker exec -it attendance-db-postgres psql -U sultan -d attendance_db
```

### Database Backup & Restore

```bash
# Backup database
docker exec attendance-db-postgres pg_dump -U sultan attendance_db > backup_$(date +%Y%m%d).sql

# Restore database
cat backup_20260202.sql | docker exec -i attendance-db-postgres psql -U sultan attendance_db

# Backup specific table
docker exec attendance-db-postgres pg_dump -U sultan -t lokasi attendance_db > lokasi_backup.sql
```

### Backend Development

```bash
# Run with auto-reload (development)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run without reload (production-like)
uvicorn main:app --host 0.0.0.0 --port 8000

# Run with custom log level
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug

# Check Python syntax
python3 -m py_compile main.py

# Run tests (if available)
pytest
```

### Logs Management

```bash
# View backend logs (real-time)
tail -f backend/logs/app_*.log

# View last 100 lines
tail -100 backend/logs/app_*.log

# Search in logs
grep "ERROR" backend/logs/app_*.log

# Clear old logs (older than 7 days)
find backend/logs/ -name "app_*.log" -mtime +7 -delete
```

## 📖 Documentation

- [Backend README](backend/README.md) - FastAPI endpoints & migrasi
- [Database README](database/README.md) - PostgreSQL Docker setup

## 📝 Next Steps

- [ ] Frontend development (React/Vue)
- [ ] Face recognition integration
- [ ] Real-time notifications
- [ ] Reports & analytics
- [ ] Mobile app


## 📝 Contoh Penggunaan API

### 🌐 Swagger UI (Recommended)

Buka **Swagger UI** untuk testing interaktif:
```
http://192.168.30.14:8000/docs
```

### 📍 Lokasi Management

#### 1. Create Lokasi Baru
```bash
curl -X POST "http://192.168.30.14:8000/api/v1/lokasi/" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_lokasi": "RSUD Sulfat - Gedung A",
    "lat": "-6.200000",
    "long": "106.816666",
    "jarak_area": 100
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Lokasi berhasil dibuat",
  "data": {
    "id_lokasi": 2,
    "nama_lokasi": "RSUD Sulfat - Gedung A",
    "lat": "-6.200000",
    "long": "106.816666",
    "jarak_area": 100
  }
}
```

#### 2. Get All Lokasi
```bash
curl http://192.168.30.14:8000/api/v1/lokasi/
```

#### 3. Get Lokasi by ID
```bash
curl http://192.168.30.14:8000/api/v1/lokasi/1
```

#### 4. Update Lokasi
```bash
curl -X PUT "http://192.168.30.14:8000/api/v1/lokasi/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_lokasi": "RSUD Sulfat - Updated",
    "jarak_area": 150
  }'
```

#### 5. Search Lokasi
```bash
curl "http://192.168.30.14:8000/api/v1/lokasi/search?q=Sulfat"
```

#### 6. Count Total Lokasi
```bash
curl http://192.168.30.14:8000/api/v1/lokasi/count
```

**Response:**
```json
{
  "success": true,
  "message": "Total lokasi berhasil diambil",
  "data": {
    "total": 5
  }
}
```

#### 7. Delete Lokasi
```bash
curl -X DELETE http://192.168.30.14:8000/api/v1/lokasi/1
```

## 📚 Troubleshooting

### ❌ Error: "connection to server failed"

**Penyebab:** `POSTGRES_HOST` di `.env` tidak sesuai dengan IP Docker

**Solusi:**
```bash
# 1. Cek IP komputer
ifconfig

# 2. Edit .env
nano .env
# Pastikan POSTGRES_HOST sesuai IP komputer yang menjalankan Docker

# 3. Restart Docker & Backend
cd database && docker compose down && docker compose up -d
cd ../backend && pkill -f uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### ❌ Error: "Missing database configuration in .env file"

**Penyebab:** File `.env` tidak lengkap atau tidak ada

**Solusi:**
```bash
# Copy dari template
cp .env.example .env

# Edit sesuai konfigurasi Anda
nano .env
```

### ❌ Error: Port already in use (98: Address already in use)

**Penyebab:** Port 5432 atau 8000 sudah digunakan

**Solusi:**
```bash
# Cek proses yang pakai port
lsof -i :5432
lsof -i :8000

# Kill process
kill -9 <PID>

# Atau untuk uvicorn
pkill -f uvicorn
```

### ❌ Docker Error: "Cannot assign requested address"

**Penyebab:** `DOCKER_HOST_IP` di `.env` pakai IP yang tidak ada

**Solusi:**
```bash
# Edit .env
nano .env

# Ganti jadi 0.0.0.0
DOCKER_HOST_IP=0.0.0.0
```

### ❌ Error: "psycopg2 not found"

**Solusi:**
```bash
pip install psycopg2-binary
```

### 🔍 Cek Status Sistem

```bash
# Docker containers
cd database && docker compose ps

# Database connection
cd backend && python3 -c "from utils.db import get_db_connection; get_db_connection().__enter__()"

# API health check
curl http://localhost:8000/api/v1/lokasi/count

# View logs
tail -f backend/logs/app_*.log
```

### 📖 Dokumentasi Lengkap

- **[CHEATSHEET.md](CHEATSHEET.md)** - Quick reference untuk command umum
- **[DOCKER_ENV_VARS.md](DOCKER_ENV_VARS.md)** - Penjelasan variabel Docker
- **[ENV_SETUP.md](ENV_SETUP.md)** - Setup guide lengkap
- **[QUICK_IP_CHANGE.md](QUICK_IP_CHANGE.md)** - Cara ganti IP dengan cepat

### GITHUB SETUP

git init
git add .
git commit -m "first commit"
git branch -M 01crud
git remote add origin https://github.com/edycoleee/fast-attendance.git
git push -u origin 01crud


---

**Made for RSUD Sulfat** 🏥
