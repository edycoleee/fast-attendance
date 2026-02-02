# Database Utilities

Modul utility untuk koneksi database PostgreSQL menggunakan `psycopg2`.

## Features

- **Context Manager**: Automatic connection management dengan `get_db_connection()`
- **RealDictCursor**: Hasil query sebagai dictionary untuk akses mudah
- **Helper Functions**: `execute_query()` dan `execute_update()` untuk operasi umum
- **Environment Variables**: Konfigurasi dari `.env` file

## Usage Examples

### 1. Basic Connection dengan Context Manager

```python
from backend.utils.db import get_db_connection, get_db_cursor

with get_db_connection() as conn:
    cursor = get_db_cursor(conn)
    cursor.execute("SELECT * FROM lokasi")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"Lokasi: {row['nama_lokasi']}")  # Access by column name
```

### 2. Execute Query (SELECT)

```python
from backend.utils.db import execute_query

# Get all records
locations = execute_query("SELECT * FROM lokasi")
for loc in locations:
    print(loc['nama_lokasi'])

# Get single record
location = execute_query(
    "SELECT * FROM lokasi WHERE id_lokasi = %s",
    (1,),
    fetch_one=True
)
print(location['nama_lokasi'])
```

### 3. Execute Update (INSERT/UPDATE/DELETE)

```python
from backend.utils.db import execute_update

# Insert new record
rows_affected = execute_update(
    """
    INSERT INTO lokasi (nama_lokasi, latitude, longitude, radius_meter)
    VALUES (%s, %s, %s, %s)
    """,
    ("Kantor Pusat", -6.2088, 106.8456, 100)
)
print(f"{rows_affected} row(s) inserted")

# Update record
execute_update(
    "UPDATE lokasi SET nama_lokasi = %s WHERE id_lokasi = %s",
    ("Kantor Cabang", 1)
)

# Delete record
execute_update(
    "DELETE FROM lokasi WHERE id_lokasi = %s",
    (1,)
)
```

### 4. Transaction Management

```python
from backend.utils.db import get_db_connection, get_db_cursor

with get_db_connection() as conn:
    cursor = get_db_cursor(conn)
    try:
        # Multiple operations in one transaction
        cursor.execute(
            "INSERT INTO lokasi (nama_lokasi, latitude, longitude) VALUES (%s, %s, %s)",
            ("Location 1", -6.2088, 106.8456)
        )
        cursor.execute(
            "INSERT INTO lokasi (nama_lokasi, latitude, longitude) VALUES (%s, %s, %s)",
            ("Location 2", -6.2100, 106.8470)
        )
        conn.commit()  # Commit all changes
    except Exception as e:
        conn.rollback()  # Rollback on error
        print(f"Error: {e}")
```

## Configuration

Database configuration menggunakan environment variables dari file `.env`:

```env
POSTGRES_DB=attendance_db
POSTGRES_USER=sultan
POSTGRES_PASSWORD=Sulfat123#!
POSTGRES_HOST=12.50.20.250
POSTGRES_PORT=5432
```

## Available Functions

### `get_db_connection()`
Context manager untuk database connection.

### `get_db_cursor(conn)`
Mendapatkan RealDictCursor dari connection.

### `execute_query(query, params=None, fetch_one=False)`
Execute SELECT query dan return results.

### `execute_update(query, params=None)`
Execute INSERT, UPDATE, atau DELETE query.

## Notes

- Selalu gunakan parameterized queries (`%s`) untuk mencegah SQL injection
- Connection otomatis ditutup oleh context manager
- RealDictCursor memungkinkan akses kolom dengan nama: `row['column_name']`
- Semua query menggunakan autocommit kecuali dalam transaction manual
