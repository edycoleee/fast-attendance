"""
Lokasi Service - Business logic layer
"""
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from repositories.lokasi_repository import LokasiRepository
from utils.logger import get_logger

logger = get_logger(__name__)


class LokasiService:
    """Service untuk business logic lokasi"""
    
    def __init__(self):
        self.repository = LokasiRepository()
    
    def create_lokasi(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create lokasi baru dengan validasi
        
        Args:
            data: Data lokasi (nama_lokasi, lat, long, jarak_area)
        
        Returns:
            Dictionary berisi data lokasi yang baru dibuat
        
        Raises:
            HTTPException: Jika terjadi error saat create
        """
        try:
            # Business logic: validasi jarak_area harus positif
            if data.get('jarak_area') is not None and data['jarak_area'] < 0:
                logger.warning(f"Invalid jarak_area: {data['jarak_area']}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Jarak area harus bernilai positif"
                )
            
            logger.debug(f"Creating lokasi with data: {data}")
            result = self.repository.create(data)
            
            if not result:
                logger.error("Failed to create lokasi - repository returned None")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Gagal membuat lokasi"
                )
            
            logger.info(f"Lokasi created successfully: {result.get('id_lokasi')}")
            return result
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating lokasi: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saat membuat lokasi: {str(e)}"
            )
    
    def get_all_lokasi(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all lokasi dengan pagination
        
        Args:
            skip: Offset untuk pagination
            limit: Maximum jumlah records (max 100)
        
        Returns:
            List of dictionaries berisi data lokasi
        """
        try:
            # Business logic: limit maksimal 100
            if limit > 100:
                limit = 100
            
            return self.repository.find_all(skip=skip, limit=limit)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saat mengambil data lokasi: {str(e)}"
            )
    
    def get_lokasi_by_id(self, id_lokasi: int) -> Dict[str, Any]:
        """
        Get lokasi by ID
        
        Args:
            id_lokasi: ID lokasi
        
        Returns:
            Dictionary berisi data lokasi
        
        Raises:
            HTTPException: 404 jika lokasi tidak ditemukan
        """
        try:
            result = self.repository.find_by_id(id_lokasi)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Lokasi dengan ID {id_lokasi} tidak ditemukan"
                )
            
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saat mengambil data lokasi: {str(e)}"
            )
    
    def update_lokasi(self, id_lokasi: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update lokasi dengan validasi
        
        Args:
            id_lokasi: ID lokasi yang akan diupdate
            data: Data yang akan diupdate
        
        Returns:
            Dictionary berisi data lokasi yang telah diupdate
        
        Raises:
            HTTPException: 404 jika lokasi tidak ditemukan
        """
        try:
            # Check if exists
            existing = self.repository.find_by_id(id_lokasi)
            if not existing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Lokasi dengan ID {id_lokasi} tidak ditemukan"
                )
            
            # Business logic: validasi jarak_area harus positif
            if data.get('jarak_area') is not None and data['jarak_area'] < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Jarak area harus bernilai positif"
                )
            
            result = self.repository.update(id_lokasi, data)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Gagal mengupdate lokasi"
                )
            
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saat mengupdate lokasi: {str(e)}"
            )
    
    def delete_lokasi(self, id_lokasi: int) -> None:
        """
        Delete lokasi
        
        Args:
            id_lokasi: ID lokasi yang akan dihapus
        
        Raises:
            HTTPException: 404 jika lokasi tidak ditemukan
        """
        try:
            # Check if exists
            existing = self.repository.find_by_id(id_lokasi)
            if not existing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Lokasi dengan ID {id_lokasi} tidak ditemukan"
                )
            
            success = self.repository.delete(id_lokasi)
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Gagal menghapus lokasi"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saat menghapus lokasi: {str(e)}"
            )
    
    def search_lokasi(self, name: str) -> List[Dict[str, Any]]:
        """
        Search lokasi by nama
        
        Args:
            name: Nama lokasi (partial match)
        
        Returns:
            List of dictionaries berisi data lokasi yang match
        """
        try:
            return self.repository.search_by_name(name)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saat mencari lokasi: {str(e)}"
            )
    
    def get_lokasi_count(self) -> int:
        """
        Get total jumlah lokasi
        
        Returns:
            Total jumlah lokasi
        """
        try:
            return self.repository.count()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saat menghitung lokasi: {str(e)}"
            )
