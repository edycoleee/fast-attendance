"""
Lokasi Repository - Data access layer dengan raw SQL queries
"""
from typing import List, Optional, Dict, Any
from config.database import get_db_connection, get_db_cursor
from utils.logger import get_logger

logger = get_logger(__name__)


class LokasiRepository:
    """Repository untuk mengelola data lokasi dengan raw SQL"""
    
    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create lokasi baru
        
        Args:
            data: Dictionary dengan keys: nama_lokasi, lat, long, jarak_area
        
        Returns:
            Dictionary berisi data lokasi yang baru dibuat
        """
        query = """
            INSERT INTO lokasi (nama_lokasi, lat, long, jarak_area)
            VALUES (%(nama_lokasi)s, %(lat)s, %(long)s, %(jarak_area)s)
            RETURNING id_lokasi, nama_lokasi, lat, long, jarak_area
        """
        
        try:
            with get_db_connection() as conn:
                cursor = get_db_cursor(conn)
                logger.debug(f"Executing INSERT query with data: {data}")
                cursor.execute(query, data)
                conn.commit()
                result = cursor.fetchone()
                logger.debug(f"Insert successful, ID: {result['id_lokasi'] if result else None}")
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Database error in create: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def find_all(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all lokasi dengan pagination
        
        Args:
            skip: Offset untuk pagination
            limit: Maximum jumlah records
        
        Returns:
            List of dictionaries berisi data lokasi
        """
        query = """
            SELECT id_lokasi, nama_lokasi, lat, long, jarak_area
            FROM lokasi
            ORDER BY id_lokasi
            LIMIT %(limit)s OFFSET %(skip)s
        """
        
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query, {'skip': skip, 'limit': limit})
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    @staticmethod
    def find_by_id(id_lokasi: int) -> Optional[Dict[str, Any]]:
        """
        Get lokasi by ID
        
        Args:
            id_lokasi: ID lokasi
        
        Returns:
            Dictionary berisi data lokasi atau None jika tidak ditemukan
        """
        query = """
            SELECT id_lokasi, nama_lokasi, lat, long, jarak_area
            FROM lokasi
            WHERE id_lokasi = %(id_lokasi)s
        """
        
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query, {'id_lokasi': id_lokasi})
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def update(id_lokasi: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update lokasi
        
        Args:
            id_lokasi: ID lokasi yang akan diupdate
            data: Dictionary dengan field yang akan diupdate
        
        Returns:
            Dictionary berisi data lokasi yang telah diupdate atau None
        """
        # Build dynamic update query
        set_clauses = []
        params = {'id_lokasi': id_lokasi}
        
        for key, value in data.items():
            if value is not None and key in ['nama_lokasi', 'lat', 'long', 'jarak_area']:
                set_clauses.append(f"{key} = %({key})s")
                params[key] = value
        
        if not set_clauses:
            return LokasiRepository.find_by_id(id_lokasi)
        
        query = f"""
            UPDATE lokasi
            SET {', '.join(set_clauses)}
            WHERE id_lokasi = %(id_lokasi)s
            RETURNING id_lokasi, nama_lokasi, lat, long, jarak_area
        """
        
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query, params)
            conn.commit()
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def delete(id_lokasi: int) -> bool:
        """
        Delete lokasi
        
        Args:
            id_lokasi: ID lokasi yang akan dihapus
        
        Returns:
            True jika berhasil dihapus, False jika tidak ditemukan
        """
        query = """
            DELETE FROM lokasi
            WHERE id_lokasi = %(id_lokasi)s
        """
        
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query, {'id_lokasi': id_lokasi})
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def count() -> int:
        """
        Count total lokasi
        
        Returns:
            Total jumlah lokasi
        """
        query = "SELECT COUNT(*) as total FROM lokasi"
        
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query)
            result = cursor.fetchone()
            return result['total'] if result else 0
    
    @staticmethod
    def search_by_name(name: str) -> List[Dict[str, Any]]:
        """
        Search lokasi by nama
        
        Args:
            name: Nama lokasi (partial match)
        
        Returns:
            List of dictionaries berisi data lokasi yang match
        """
        query = """
            SELECT id_lokasi, nama_lokasi, lat, long, jarak_area
            FROM lokasi
            WHERE nama_lokasi ILIKE %(name)s
            ORDER BY nama_lokasi
        """
        
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(query, {'name': f'%{name}%'})
            results = cursor.fetchall()
            return [dict(row) for row in results]
