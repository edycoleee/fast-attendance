# Database - PostgreSQL with Docker

PostgreSQL database untuk sistem attendance RSUD Sulfat dengan pgAdmin.

**Schema**: Converted from MySQL RSUD Sulfat (17 tables + 3 views)

## 🚀 Quick Start

```powershell
# Start database
docker-compose up -d

# Check status
docker-compose ps

# Stop database
docker-compose down

# Stop and remove all data
docker-compose down -v
```

## 📋 Akses Database

### PostgreSQL
- **Host**: `12.50.20.250:5432`
- **Database**: `attendance_db`
- **User**: `sultan`
- **Password**: `Sulfat123#!`

**Connection String:**
```
postgresql://sultan:Sulfat123#!@12.50.20.250:5432/attendance_db
```

### pgAdmin (Web Interface)
- **URL**: http://12.50.20.250:5050
- **Email**: admin@admin.com
- **Password**: admin

**Cara menambahkan server di pgAdmin:**
1. Buka http://12.50.20.250:5050
2. Login dengan email/password di atas
3. Klik kanan "Servers" → "Register" → "Server"
4. **General Tab**: Name = `Attendance DB`
5. **Connection Tab**:
   - Host = `postgres` (nama service di docker)
   - Port = `5432`
   - Database = `attendance_db`
   - Username = `sultan`
   - Password = `Sulfat123#!`
6. Save

## 📁 File Structure

```
database/
├── docker-compose.yml   # Docker configuration
├── init.sql            # Initialization script (auto-run on first start)
└── README.md           # This file
```

## 🔧 Docker Commands

```powershell
# View logs
docker-compose logs -f postgres
docker-compose logs -f pgadmin

# Restart service
docker-compose restart postgres


# In psql - explore tables
\dt              # List all tables
\dv              # List all views
\d pegawai       # Describe pegawai table
SELECT * FROM ruang;
SELECT * FROM v_shift;
\q
# Execute SQL directly
docker exec -it attendance-db-postgres psql -U sultan -d attendance_db

# Backup database
docker exec attendance-db-postgres pg_dump -U sultan attendance_db > backup.sql

# Restore database
cat backup.sql | docker exec -i attendance-db-postgres psql -U sultan attendance_db
```

## 📊 Database Schema

**Total: 17 Tables + 3 Views**

### Main Tables

#### Table: pegawai (Employee)
```sql
CREATE TABLE pegawai (
    id_pegawai VARCHAR(20) PRIMARY KEY,
    nip VARCHAR(255),
    nama VARCHAR(255),
    jenis_kelamin VARCHAR(255),
    tempat_lahir VARCHAR(255),
    tanggal_lahir DATE,
    alamat TEXT,
    id_ruang INTEGER,
    status VARCHAR(15),
    create_at VARCHAR(255),
    create_date TIMESTAMP,
    foto VARCHAR(100)
);
```

#### Table: absensi (Attendance)
```sql
CREATE TABLE absensi (
    id_absensi VARCHAR(11) PRIMARY KEY,
    id_lokasi INTEGER,
    id_pegawai VARCHAR(20),
    uid VARCHAR(30),
    tanggal TIMESTAMP,
    ket VARCHAR(50),
    ipaddress VARCHAR(20)
);
```

#### Table: shift
```sql
CREATE TABLE shift (
    id_shift SERIAL PRIMARY KEY,
    nama_shift VARCHAR(255),
    jam_masuk VARCHAR(255),
    jam_keluar VARCHAR(255)
);
```

#### Table: detail_shift_pegawai
```sql
CREATE TABLE detail_shift_pegawai (
    id_detail_shift_pegawai VARCHAR(20) PRIMARY KEY,
    id_shift_pegawai VARCHAR(20),
    id_pegawai VARCHAR(20),
    hari01 VARCHAR(20),
    hari02 VARCHAR(20),
    -- ... hari03 to hari31
);
```

### Other Tschema converted from **MySQL RSUD Sulfat** to PostgreSQL
- Total **17 tables** and **3 views** for complete attendance system
- Database menggunakan **pgvector** extension (untuk future face recognition features)
- Schema includes: employees, attendance, shifts, locations, messaging, and user management
- Data persistent di Docker volume `postgres_data`
- Init script ([init.sql](init.sql)) runs automatically on first container star
- **shift_pegawai** - Monthly shift schedules
- **keterangan_absen** - Attendance notes/reasons
- **login_absensi** - Mobile login devices
- **pesan** - Messages/announcements
- **pesan_detail** - Message read status
- **user** - User accounts
- **userlevels** - User roles
- **userlevelpermissions** - Role permissions

### Views
- **v_shift** - Shift information with formatted time
- **v_shiftpeg** - Unpivoted shift schedule (31 days)
- **v_user_pegawai** - User-employee join view

**Full schema**: See [init.sql](init.sql)

## 🔍 Troubleshooting

### Port already in use
```powershell
# Check what's using port 5432 or 5050
netstat -ano | findstr :5432
netstat -ano | findstr :5050

# Kill process
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Can't connect from backend
- Pastikan IP `12.50.20.250` adalah IP network adapter yang benar
- Cek dengan: `ipconfig`
- Update di docker-compose.yml jika perlu

### Reset everything
```powershell
docker-compose down -v
docker-compose up -d
```

## 📝 Notes

- Database menggunakan **pgvector** extension (untuk future face recognition features)
- Data persistent di Docker volume `postgres_data`
- Init script hanya run sekali saat pertama kali container dibuat
- Untuk re-run init.sql, hapus volume: `docker-compose down -v`
