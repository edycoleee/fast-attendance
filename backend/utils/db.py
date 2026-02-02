"""
Database utility module for PostgreSQL connection using psycopg2.
Provides direct database access with RealDictCursor for dict-like results.
"""
import psycopg2
import psycopg2.extras
import os
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables from parent directory
import sys
from pathlib import Path

# Add parent directory to path for .env file
root_dir = Path(__file__).parent.parent.parent
load_dotenv(dotenv_path=root_dir / '.env')

# PostgreSQL connection configuration
# Load dari .env file - WAJIB ada .env file di root project
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT')
}

# Validasi konfigurasi database
if not all(DB_CONFIG.values()):
    missing = [k for k, v in DB_CONFIG.items() if not v]
    raise ValueError(
        f"Missing database configuration in .env file: {', '.join(missing)}\n"
        f"Please create/update .env file in project root with:\n"
        f"  POSTGRES_DB=attendance_db\n"
        f"  POSTGRES_USER=sultan\n"
        f"  POSTGRES_PASSWORD=yourpassword\n"
        f"  POSTGRES_HOST=192.168.30.14  # Ganti sesuai IP komputer Docker\n"
        f"  POSTGRES_PORT=5432"
    )


@contextmanager
def get_db_connection():
    """
    Context manager untuk PostgreSQL connection.
    Menggunakan psycopg2 dengan RealDictCursor untuk hasil query seperti dict.
    
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    
    Yields:
        psycopg2.connection: Database connection object
    """
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


def get_db_cursor(conn):
    """
    Get cursor dengan RealDictCursor untuk hasil query sebagai dict.
    Mirip dengan sqlite3.Row behavior.
    
    Args:
        conn: psycopg2 connection object
    
    Returns:
        psycopg2.extras.RealDictCursor: Cursor dengan hasil dict-like
    
    Example:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("SELECT * FROM lokasi")
            rows = cursor.fetchall()
            for row in rows:
                print(row['nama_lokasi'])  # Access by column name
    """
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def execute_query(query, params=None, fetch_one=False):
    """
    Execute a SELECT query and return results.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters for prepared statements
        fetch_one (bool): If True, return single row; if False, return all rows
    
    Returns:
        dict or list: Query results as dict (fetch_one=True) or list of dicts
    
    Example:
        # Get all locations
        locations = execute_query("SELECT * FROM lokasi")
        
        # Get one location by ID
        location = execute_query(
            "SELECT * FROM lokasi WHERE id_lokasi = %s",
            (1,),
            fetch_one=True
        )
    """
    with get_db_connection() as conn:
        cursor = get_db_cursor(conn)
        cursor.execute(query, params)
        if fetch_one:
            return cursor.fetchone()
        return cursor.fetchall()


def execute_update(query, params=None):
    """
    Execute an INSERT, UPDATE, or DELETE query.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters for prepared statements
    
    Returns:
        int: Number of rows affected
    
    Example:
        # Insert new location
        rows_affected = execute_update(
            "INSERT INTO lokasi (nama_lokasi, latitude, longitude) VALUES (%s, %s, %s)",
            ("Main Office", -6.2088, 106.8456)
        )
        
        # Update location
        execute_update(
            "UPDATE lokasi SET nama_lokasi = %s WHERE id_lokasi = %s",
            ("New Name", 1)
        )
    """
    with get_db_connection() as conn:
        cursor = get_db_cursor(conn)
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
