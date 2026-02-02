# Environment Setup Guide

## 🔧 Cara Ganti Konfigurasi Database Saat Pindah Komputer

### File Penting: `.env`
File `.env` berisi konfigurasi database yang perlu disesuaikan saat berpindah komputer.

---

## 📝 Langkah Setup

### 1. Cek IP Komputer/Raspberry Pi yang Menjalankan Docker

```bash
# Untuk Raspberry Pi / Linux
ifconfig

# Atau
ip addr show

# Cari IP address di network interface (biasanya eth0 atau wlan0)
# Contoh output: inet 192.168.30.14/24
```

### 2. Edit File `.env` di Root Project

```bash
nano /home/sultan/fast/fast-attendance/.env
```

### 3. Ganti `POSTGRES_HOST` Sesuai Situasi

**Skenario A: Raspberry Pi (Docker berjalan di Raspberry Pi)**
```env
POSTGRES_HOST=192.168.30.14  # IP Raspberry Pi di network
```

**Skenario B: Development di Laptop Lokal**
```env
POSTGRES_HOST=localhost
# atau
POSTGRES_HOST=127.0.0.1
```

**Skenario C: Server Lain di Network**
```env
POSTGRES_HOST=192.168.30.100  # IP server yang menjalankan Docker
```

### 4. Restart Docker dan Backend

```bash
# 1. Restart Docker containers
cd /home/sultan/fast/fast-attendance/database
docker compose down
docker compose up -d

# 2. Tunggu PostgreSQL ready (5-10 detik)
sleep 5
docker compose ps

# 3. Restart FastAPI backend
cd /home/sultan/fast/fast-attendance/backend
pkill -f "uvicorn main:app"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📋 Konfigurasi Lengkap di `.env`

```env
# ============================================================
# PostgreSQL Database Configuration
# ============================================================
POSTGRES_DB=attendance_db
POSTGRES_USER=sultan
POSTGRES_PASSWORD=Sulfat123#!
POSTGRES_HOST=192.168.30.14    # 🔴 GANTI INI SESUAI IP KOMPUTER DOCKER
POSTGRES_PORT=5432

# ============================================================
# Database URL (for SQLAlchemy)
# ============================================================
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# ============================================================
# pgAdmin Configuration
# ============================================================
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
PGADMIN_PORT=5050
```

---

## 🚀 Quick Setup untuk Komputer Baru

```bash
# 1. Clone project
git clone <repository-url>
cd fast-attendance

# 2. Copy .env template (jika ada .env.example)
cp .env.example .env

# 3. Edit .env - WAJIB ganti POSTGRES_HOST
nano .env
# Ganti: POSTGRES_HOST=192.168.30.14  # sesuai IP komputer ini

# 4. Start Docker database
cd database
docker compose up -d

# 5. Install Python dependencies
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Start FastAPI server
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ Verifikasi Setup

### Cek Docker Running
```bash
docker compose ps
# Harus ada 2 containers: postgres (healthy) dan pgadmin
```

### Test Database Connection
```bash
cd backend
python3 -c "
from utils.db import get_db_connection, get_db_cursor
with get_db_connection() as conn:
    cursor = get_db_cursor(conn)
    cursor.execute('SELECT 1 as test')
    print('✓ Database connected:', cursor.fetchone())
"
```

### Test API Endpoint
```bash
curl http://localhost:8000/api/v1/lokasi/count
# Harus return JSON response
```

---

## 🔍 Troubleshooting

### Error: "connection to server failed"
**Penyebab:** `POSTGRES_HOST` salah atau Docker belum running

**Solusi:**
1. Cek Docker: `docker compose ps`
2. Cek IP di .env sesuai dengan komputer yang menjalankan Docker
3. Restart: `docker compose down && docker compose up -d`

### Error: "Missing database configuration in .env file"
**Penyebab:** File `.env` tidak ada atau variabel tidak lengkap

**Solusi:**
1. Cek file ada: `ls -la /home/sultan/fast/fast-attendance/.env`
2. Cek isi lengkap: `cat /home/sultan/fast/fast-attendance/.env`
3. Pastikan semua variabel POSTGRES_* ada

### Port sudah terpakai (Error 98: Address already in use)
**Solusi:**
```bash
# Cari proses yang pakai port
lsof -i :8000
lsof -i :5432

# Kill proses
kill -9 <PID>
```

---

## 📌 Catatan Penting

1. **Jangan commit `.env` ke Git!** 
   - File ini berisi password dan konfigurasi lokal
   - Gunakan `.env.example` sebagai template

2. **Backup `.env` saat pindah komputer**
   - Copy `.env` ke komputer baru
   - Edit `POSTGRES_HOST` sesuai IP komputer baru

3. **Network Access**
   - Pastikan firewall allow port 5432 (PostgreSQL)
   - Raspberry Pi dan komputer client harus di network yang sama

4. **Docker Compose Auto-Load .env**
   - Docker compose otomatis load `.env` dari parent directory
   - Tidak perlu edit `docker-compose.yml` saat ganti IP

---

**Lokasi File Penting:**
- `.env`: `/home/sultan/fast/fast-attendance/.env`
- Docker compose: `/home/sultan/fast/fast-attendance/database/docker-compose.yml`
- Backend DB config: `/home/sultan/fast/fast-attendance/backend/utils/db.py`
