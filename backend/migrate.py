"""
Script untuk migrasi data dari MySQL ke PostgreSQL
"""
import mysql.connector
import psycopg2
from datetime import datetime

# Konfigurasi MySQL
MYSQL_CONFIG = {
    'host': '192.10.10.15',
    'port': 3306,
    'user': 'rsudsulfat',
    'password': 'rsudsulfat123',
    'database': 'rsud_sulfat'
}

# Konfigurasi PostgreSQL (Docker)
POSTGRES_CONFIG = {
    'host': '12.50.20.250',
    'port': 5432,
    'user': 'sultan',
    'password': 'Sulfat123#!',
    'database': 'attendance_db'
}

def migrate_data():
    # Koneksi ke MySQL
    mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    
    # Koneksi ke PostgreSQL
    pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
    pg_cursor = pg_conn.cursor()
    
    print("Migrasi dimulai...")
    
    # Migrasi tabel employees
    print("\n1. Migrasi tabel employees...")
    mysql_cursor.execute("SELECT * FROM employees")
    employees = mysql_cursor.fetchall()
    
    for emp in employees:
        pg_cursor.execute("""
            INSERT INTO employees (id, employee_id, name, email, department, position, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            emp['id'], emp['employee_id'], emp['name'], emp['email'],
            emp['department'], emp['position'], emp['is_active'],
            emp['created_at'], emp.get('updated_at')
        ))
    
    pg_conn.commit()
    print(f"   ✓ {len(employees)} employees berhasil dimigrasikan")
    
    # Migrasi tabel attendances
    print("\n2. Migrasi tabel attendances...")
    mysql_cursor.execute("SELECT * FROM attendances")
    attendances = mysql_cursor.fetchall()
    
    for att in attendances:
        pg_cursor.execute("""
            INSERT INTO attendances (id, employee_id, check_in, check_out, status, notes, location, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            att['id'], att['employee_id'], att['check_in'], att['check_out'],
            att['status'], att.get('notes'), att.get('location'),
            att['created_at'], att.get('updated_at')
        ))
    
    pg_conn.commit()
    print(f"   ✓ {len(attendances)} attendance records berhasil dimigrasikan")
    
    # Reset sequences
    print("\n3. Reset sequences...")
    pg_cursor.execute("""
        SELECT setval('employees_id_seq', (SELECT MAX(id) FROM employees));
    """)
    pg_cursor.execute("""
        SELECT setval('attendances_id_seq', (SELECT MAX(id) FROM attendances));
    """)
    pg_conn.commit()
    print("   ✓ Sequences berhasil direset")
    
    # Tutup koneksi
    mysql_cursor.close()
    mysql_conn.close()
    pg_cursor.close()
    pg_conn.close()
    
    print("\n✅ Migrasi selesai!")

if __name__ == "__main__":
    try:
        migrate_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPastikan:")
        print("1. MySQL dan PostgreSQL sudah berjalan")
        print("2. Konfigurasi database sudah benar")
        print("3. Tabel sudah dibuat di PostgreSQL (jalankan aplikasi sekali)")
        print("4. Install: pip install mysql-connector-python psycopg2-binary")
