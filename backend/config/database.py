"""
Database configuration and connection management
"""
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings

# ============================================================
# SQLAlchemy Setup (for ORM if needed)
# ============================================================
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for SQLAlchemy session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# psycopg2 Setup (for raw SQL queries)
# ============================================================

@contextmanager
def get_db_connection():
    """
    Context manager untuk PostgreSQL connection.
    Menggunakan psycopg2 dengan RealDictCursor untuk hasil query seperti dict.
    
    Usage:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("SELECT * FROM lokasi")
            results = cursor.fetchall()
    """
    conn = psycopg2.connect(**settings.DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


def get_db_cursor(conn):
    """
    Get cursor dengan RealDictCursor untuk hasil query sebagai dict.
    
    Args:
        conn: psycopg2 connection object
    
    Returns:
        psycopg2.extras.RealDictCursor: Cursor dengan hasil dict-like
    """
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
