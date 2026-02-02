# 🔧 Docker Port Binding dengan Environment Variables

## Penjelasan Variabel

### 1. `DOCKER_HOST_IP` (Baru!)
**Fungsi:** Menentukan IP mana Docker akan **listen/binding** port

**Pilihan:**
```env
# Listen di SEMUA interface (recommended - bisa diakses dari mana saja)
DOCKER_HOST_IP=0.0.0.0

# Listen hanya di IP tertentu (hanya bisa diakses lewat IP ini)
DOCKER_HOST_IP=192.168.30.14

# Listen hanya localhost (hanya bisa diakses dari komputer ini)
DOCKER_HOST_IP=127.0.0.1
```

**Kapan Pakai Apa?**
- **0.0.0.0** → Bisa diakses dari localhost DAN komputer lain di network ✅ Recommended
- **192.168.30.14** → Hanya bisa diakses lewat IP ini (tidak bisa via localhost)
- **127.0.0.1** → Hanya bisa diakses dari komputer yang sama (tidak bisa dari network)

### 2. `POSTGRES_HOST`
**Fungsi:** IP yang digunakan oleh **backend untuk connect** ke database

**Pilihan:**
```env
# Jika backend & Docker di komputer yang sama
POSTGRES_HOST=localhost

# Jika backend di komputer lain, Docker di Raspberry Pi
POSTGRES_HOST=192.168.30.14

# Jika backend di Docker container (future: docker-compose full stack)
POSTGRES_HOST=postgres  # nama service di docker-compose
```

---

## 🎯 Skenario Penggunaan

### Scenario A: Development Lokal (Semua di 1 Komputer)
```env
DOCKER_HOST_IP=0.0.0.0      # Docker listen di semua interface
POSTGRES_HOST=localhost      # Backend connect ke localhost
```

**Akses:**
- Backend → Database: `localhost:5432` ✅
- pgAdmin: `http://localhost:5050` ✅
- API: `http://localhost:8000` ✅

---

### Scenario B: Raspberry Pi + Akses dari Laptop Lain
```env
DOCKER_HOST_IP=0.0.0.0           # Docker listen di semua interface
POSTGRES_HOST=192.168.30.14      # Backend connect ke IP Raspberry Pi
```

**Akses dari Raspberry Pi:**
- Backend → Database: `192.168.30.14:5432` ✅
- pgAdmin: `http://192.168.30.14:5050` ✅
- API: `http://192.168.30.14:8000` ✅

**Akses dari Laptop Lain di Network:**
- pgAdmin: `http://192.168.30.14:5050` ✅
- API: `http://192.168.30.14:8000` ✅

---

### Scenario C: Security - Hanya Localhost (Untuk Testing)
```env
DOCKER_HOST_IP=127.0.0.1    # Docker HANYA listen localhost
POSTGRES_HOST=localhost      # Backend connect ke localhost
```

**Akses:**
- Backend → Database: `localhost:5432` ✅
- pgAdmin: `http://localhost:5050` ✅
- API: `http://localhost:8000` ✅
- **Dari komputer lain: ❌ TIDAK BISA**

---

## 📝 Cara Kerja di Docker Compose

### File: `docker-compose.yml`
```yaml
services:
  postgres:
    ports:
      - "${DOCKER_HOST_IP:-0.0.0.0}:5432:5432"
      #  ↑ Dari .env file     ↑ Default jika tidak ada di .env
```

**Penjelasan:**
- `${DOCKER_HOST_IP}` → Ambil nilai dari file `.env`
- `:-0.0.0.0` → Jika variabel tidak ada, pakai `0.0.0.0` sebagai default
- `5432:5432` → Map port 5432 container ke port 5432 host

### Format Port Binding
```
[HOST_IP:]HOST_PORT:CONTAINER_PORT
```

**Contoh:**
- `"5432:5432"` → Sama dengan `"0.0.0.0:5432:5432"` (semua interface)
- `"192.168.30.14:5432:5432"` → Hanya listen di IP 192.168.30.14
- `"127.0.0.1:5432:5432"` → Hanya listen di localhost

---

## 🔄 Cara Ganti Konfigurasi

### 1. Edit `.env`
```bash
nano /home/sultan/fast/fast-attendance/.env
```

### 2. Ganti Variabel yang Diperlukan
```env
# Untuk akses dari network
DOCKER_HOST_IP=0.0.0.0
POSTGRES_HOST=192.168.30.14

# Untuk development lokal
DOCKER_HOST_IP=0.0.0.0
POSTGRES_HOST=localhost
```

### 3. Restart Docker
```bash
cd /home/sultan/fast/fast-attendance/database
docker compose down
docker compose up -d
```

### 4. Restart Backend (jika POSTGRES_HOST berubah)
```bash
cd /home/sultan/fast/fast-attendance/backend
pkill -f uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ Verification

### Cek Variabel Ter-Load
```bash
cd /home/sultan/fast/fast-attendance/database
docker compose config | grep host_ip
```

Output yang benar:
```yaml
host_ip: 0.0.0.0  # Atau sesuai DOCKER_HOST_IP di .env
```

### Cek Port Listening
```bash
# PostgreSQL
netstat -tulpn | grep 5432

# pgAdmin
netstat -tulpn | grep 5050
```

Output jika DOCKER_HOST_IP=0.0.0.0:
```
tcp  0  0  0.0.0.0:5432  0.0.0.0:*  LISTEN
tcp  0  0  0.0.0.0:5050  0.0.0.0:*  LISTEN
```

Output jika DOCKER_HOST_IP=127.0.0.1:
```
tcp  0  0  127.0.0.1:5432  0.0.0.0:*  LISTEN
tcp  0  0  127.0.0.1:5050  0.0.0.0:*  LISTEN
```

---

## 🎓 Best Practices

1. **Development:** Gunakan `DOCKER_HOST_IP=0.0.0.0` untuk fleksibilitas
2. **Production:** Gunakan IP spesifik atau firewall rules untuk security
3. **Testing:** Gunakan `127.0.0.1` untuk isolasi lengkap
4. **Consistency:** `POSTGRES_HOST` harus match dengan IP yang bisa diakses oleh backend

---

## 🔍 Troubleshooting

### Problem: "Connection refused" dari komputer lain
**Penyebab:** `DOCKER_HOST_IP` mungkin `127.0.0.1`

**Solusi:**
```env
DOCKER_HOST_IP=0.0.0.0  # Ganti jadi 0.0.0.0
```

### Problem: Backend tidak bisa connect ke database
**Penyebab:** `POSTGRES_HOST` salah

**Solusi:**
- Jika backend & Docker di komputer sama: `POSTGRES_HOST=localhost`
- Jika backend di komputer lain: `POSTGRES_HOST=<IP_DOCKER_SERVER>`

### Problem: "Cannot assign requested address"
**Penyebab:** `DOCKER_HOST_IP` pakai IP yang tidak ada di komputer

**Solusi:**
```bash
# Cek IP yang ada
ip addr show

# Gunakan IP yang valid atau 0.0.0.0
```

---

**Updated:** 2 February 2026
**Feature:** Docker Compose Variable Substitution from .env
