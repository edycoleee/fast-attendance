# 🚀 Quick Start - Ganti IP Database

## Saat Pindah Komputer/Server

### 1. Cek IP Komputer
```bash
ifconfig
# Atau
ip addr show
# Cari IP di eth0/wlan0 (contoh: 192.168.30.14)
```

### 2. Edit `.env` - HANYA 1 BARIS!
```bash
nano .env
```

Ganti baris ini:
```env
POSTGRES_HOST=192.168.30.14  # ← GANTI INI SAJA
```

### 3. Restart Everything
```bash
# Restart Docker
cd database
docker compose down && docker compose up -d

# Restart Backend
cd ../backend
pkill -f uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Contoh Konfigurasi

**Raspberry Pi (IP: 192.168.30.14)**
```env
POSTGRES_HOST=192.168.30.14
```

**Laptop Development (lokal)**
```env
POSTGRES_HOST=localhost
```

**Server Lain (IP: 192.168.30.100)**
```env
POSTGRES_HOST=192.168.30.100
```

---

## Test Koneksi

```bash
# Test database
cd backend
python3 -c "from utils.db import get_db_connection; conn = get_db_connection().__enter__(); print('✓ OK')"

# Test API
curl http://localhost:8000/api/v1/lokasi/count
```

---

**Dokumentasi Lengkap:** [ENV_SETUP.md](ENV_SETUP.md)
