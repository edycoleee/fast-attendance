# 🚀 Cheat Sheet - Fast Attendance System

## 📝 Edit .env (Saat Pindah Komputer)

```bash
nano /home/sultan/fast/fast-attendance/.env
```

**Yang Perlu Diganti:**

| Variable | Fungsi | Nilai Biasa |
|----------|--------|-------------|
| `DOCKER_HOST_IP` | IP Docker binding | `0.0.0.0` (semua interface) |
| `POSTGRES_HOST` | IP untuk connect DB | `localhost` atau `192.168.30.14` |

---

## 🔄 Restart Services

### Docker (Setelah Edit .env)
```bash
cd /home/sultan/fast/fast-attendance/database
docker compose down && docker compose up -d
```

### Backend (Setelah Edit POSTGRES_HOST)
```bash
cd /home/sultan/fast/fast-attendance/backend
pkill -f uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ Quick Test

```bash
# Test database
python3 -c "from utils.db import get_db_connection; get_db_connection().__enter__()"

# Test API
curl http://localhost:8000/api/v1/lokasi/count
```

---

## 🎯 Common Scenarios

### Local Development
```env
DOCKER_HOST_IP=0.0.0.0
POSTGRES_HOST=localhost
```

### Raspberry Pi + Remote Access
```env
DOCKER_HOST_IP=0.0.0.0
POSTGRES_HOST=192.168.30.14
```

### Localhost Only (Secure)
```env
DOCKER_HOST_IP=127.0.0.1
POSTGRES_HOST=localhost
```

---

## 📍 Access URLs

| Service | URL | Default Login |
|---------|-----|---------------|
| API Docs | http://192.168.30.14:8000/docs | - |
| pgAdmin | http://192.168.30.14:5050 | admin@admin.com / admin |
| PostgreSQL | 192.168.30.14:5432 | sultan / Sulfat123#! |

---

## 📖 Full Documentation

- [DOCKER_ENV_VARS.md](DOCKER_ENV_VARS.md) - Docker variables explained
- [QUICK_IP_CHANGE.md](QUICK_IP_CHANGE.md) - IP change guide
- [ENV_SETUP.md](ENV_SETUP.md) - Complete setup guide
