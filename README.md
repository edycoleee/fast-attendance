# RSUD Sulfat - Fast Attendance System

Sistem attendance dengan PostgreSQL (Docker) untuk RSUD Sulfat.

## 📁 Project Structure

```
fast-attendace/
├── backend/          # FastAPI backend
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── migrate.py
│   └── requirements.txt
├── database/         # PostgreSQL Docker
│   ├── docker-compose.yml
│   └── init.sql
├── frontend/         # React/Vue (coming soon)
└── README.md
```

## 🚀 Quick Start

### 1️⃣ Start Database (PostgreSQL dengan Docker)

```powershell
cd database
docker-compose up -d
```

**Akses Database:**
- PostgreSQL: `12.50.20.250:5432`
- pgAdmin: http://12.50.20.250:5050 (admin@admin.com / admin)

### 2️⃣ Setup Backend

```powershell
cd backend
pip install -r requirements.txt
```

### 3️⃣ Migrasi Data dari MySQL RSUD Sulfat (Opsional)

Jika ada data di MySQL lama:

```powershell
cd backend
pip install mysql-connector-python
python migrate.py
```

### 4️⃣ Run Backend

```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API Documentation**: http://localhost:8000/docs

## 🔧 Konfigurasi

### Database Source (MySQL RSUD Sulfat)
- Host: `192.10.10.15:3306`
- Database: `rsud_sulfat`
- User: `rsudsulfat`
- Password: `rsudsulfat123`

### Database Target (PostgreSQL Docker)
- Host: `12.50.20.250:5432`
- Database: `attendance_db`
- User: `sultan`
- Password: `Sulfat123#!`

## 📊 Database Schema

### employees
- employee_id, name, email, department, position
- is_active, created_at, updated_at

### attendances
- employee_id, check_in, check_out
- status, notes, location
- created_at, updated_at

## 🔧 API Endpoints

### Employees
- `POST /employees/` - Buat employee baru
- `GET /employees/` - List semua employees
- `GET /employees/{id}` - Detail employee
- `PUT /employees/{id}` - Update employee
- `DELETE /employees/{id}` - Hapus employee

### Attendances
- `POST /attendances/` - Check-in (buat record baru)
- `GET /attendances/` - List semua attendance
- `GET /attendances/{id}` - Detail attendance
- `PUT /attendances/{id}` - Update (check-out)
- `GET /attendances/employee/{employee_id}` - Attendance per employee

## 🛠️ Development Commands

### Database Management
```powershell
# Stop database
cd database
docker-compose down

# View logs
docker-compose logs -f postgres

# Reset database (hapus semua data)
docker-compose down -v
docker-compose up -d

# Backup database
docker exec attendance-db-postgres pg_dump -U sultan attendance_db > backup.sql

# Restore database
Get-Content backup.sql | docker exec -i attendance-db-postgres psql -U sultan attendance_db
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

## 🔐 Security Notes

- ⚠️ Ganti password default sebelum production
- ⚠️ Jangan commit file `.env` ke git
- ⚠️ Gunakan HTTPS di production
- ⚠️ Setup firewall rules untuk Docker ports
- `PUT /employees/{id}` - Update employee
- `DELETE /employees/{id}` - Hapus employee

### Attendances
- `POST /attendances/` - Check-in (buat record baru)
- `GET /attendances/` - List semua attendance
- `GET /attendances/{id}` - Detail attendance
- `PUT /attendances/{id}` - Update (check-out)
- `GET /attendances/employee/{employee_id}` - Attendance per employee

## 📝 Contoh Penggunaan API

Buka **Swagger UI** di http://localhost:8000/docs untuk testing interaktif!

### Buat Employee:
```powershell
curl -X POST "http://localhost:8000/employees/" -H "Content-Type: application/json" -d '{\"employee_id\":\"EMP001\",\"name\":\"Dr. Ahmad\",\"email\":\"ahmad@rsudsulfat.com\",\"department\":\"Medical\",\"position\":\"Doctor\"}'
```

### Check-in:
```powershell
curl -X POST "http://localhost:8000/attendances/" -H "Content-Type: application/json" -d '{\"employee_id\":1,\"check_in\":\"2026-02-02T08:00:00\",\"status\":\"present\",\"location\":\"RSUD Sulfat\"}'
```

### Check-out:
```powershell
curl -X PUT "http://localhost:8000/attendances/1" -H "Content-Type: application/json" -d '{\"check_out\":\"2026-02-02T17:00:00\"}'
```

## 📚 Troubleshooting

### Database Error: "Can't connect to server"
```powershell
# Cek PostgreSQL Docker
cd database
docker-compose ps

# Restart jika perlu
docker-compose restart postgres
```

### Error: "psycopg2 not found"
```powershell
pip install psycopg2-binary
```

### Error: Port already in use
```powershell
# Check what's using the port
netstat -ano | findstr :5432
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```


git init
git add .
git commit -m "first commit"
git branch -M 01crud
git remote add origin https://github.com/edycoleee/fast-attendance.git
git push -u origin 01crud


---

**Made for RSUD Sulfat** 🏥
