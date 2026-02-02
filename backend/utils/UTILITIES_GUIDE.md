# Utils - Standard Response, Logger & Middleware

Dokumentasi untuk utilities: standard response format, logging, dan middleware.

## 📦 Modules

### 1. Response (`utils/response.py`)

Standard response format untuk semua API endpoints.

#### Functions

**success_response(message, data, status_code)**
```python
from utils.response import success_response

return success_response(
    message="Data berhasil diambil",
    data={"id": 1, "nama": "Test"}
)

# Output:
{
    "success": true,
    "message": "Data berhasil diambil",
    "data": {"id": 1, "nama": "Test"}
}
```

**error_response(message, data, status_code)**
```python
from utils.response import error_response

return error_response(
    message="Data tidak ditemukan",
    data={"error": "Not found"}
)

# Output:
{
    "success": false,
    "message": "Data tidak ditemukan",
    "data": {"error": "Not found"}
}
```

**paginated_response(message, data, page, limit, total)**
```python
from utils.response import paginated_response

return paginated_response(
    message="Lokasi berhasil diambil",
    data=[...],
    page=1,
    limit=10,
    total=50
)

# Output:
{
    "success": true,
    "message": "Lokasi berhasil diambil",
    "data": [...],
    "meta": {
        "page": 1,
        "limit": 10,
        "total": 50,
        "total_pages": 5
    }
}
```

### 2. Logger (`utils/logger.py`)

Logging configuration untuk aplikasi.

#### Usage

**Basic logging**
```python
from utils.logger import logger

logger.info("This is an info message")
logger.error("This is an error message")
logger.warning("This is a warning")
logger.debug("This is debug info")
```

**Get named logger**
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info(f"Processing request: {request_id}")
```

**Log exception**
```python
from utils.logger import log_exception

try:
    # some code
    pass
except Exception as e:
    log_exception(f"Error processing data: {str(e)}")
```

#### Log Files

Logs disimpan di: `backend/logs/app_YYYYMMDD.log`

Format: `YYYY-MM-DD HH:MM:SS - module_name - LEVEL - message`

Example:
```
2026-02-02 19:55:30 - api.v1.endpoints.lokasi - INFO - Creating new lokasi: RSUD Sulfat
2026-02-02 19:55:31 - services.lokasi_service - INFO - Lokasi created successfully: 1
```

### 3. Middleware (`utils/middleware.py`)

Request logging middleware untuk track semua HTTP requests.

#### Features

- ✅ Log setiap request (method, path, client IP)
- ✅ Log response (status code, process time)
- ✅ Add `X-Process-Time` header to response
- ✅ Log errors with traceback

#### Auto-enabled

Middleware sudah di-enable di `main.py`, tidak perlu konfigurasi tambahan.

#### Log Output

```
INFO - Request: GET /api/v1/lokasi/ from 127.0.0.1
INFO - Response: GET /api/v1/lokasi/ Status: 200 Time: 0.023s
```

### 4. Exception Handlers (`utils/exception_handlers.py`)

Global exception handlers untuk FastAPI.

#### Handlers

**HTTP Exception Handler**
- Handle HTTPException dari FastAPI
- Return standard error response

**Validation Exception Handler**
- Handle Pydantic validation errors
- Format validation errors dengan field details

**General Exception Handler**
- Handle semua unhandled exceptions
- Log dengan traceback
- Return 500 error

#### Auto-enabled

Exception handlers sudah di-register di `main.py`.

#### Example Output

Validation error:
```json
{
    "success": false,
    "message": "Validation error",
    "data": {
        "errors": [
            {
                "field": "jarak_area",
                "message": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }
}
```

## 🔧 Usage Examples

### Endpoint dengan Standard Response

```python
# api/v1/endpoints/lokasi.py
from utils.response import success_response, paginated_response
from utils.logger import get_logger

logger = get_logger(__name__)

@router.post("/")
def create_lokasi(lokasi: LokasiCreate):
    logger.info(f"Creating lokasi: {lokasi.nama_lokasi}")
    result = lokasi_service.create_lokasi(lokasi.model_dump())
    
    return success_response(
        message="Lokasi berhasil dibuat",
        data=result
    )

@router.get("/")
def get_all_lokasi(skip: int = 0, limit: int = 10):
    logger.info(f"Fetching lokasi: skip={skip}, limit={limit}")
    
    data = lokasi_service.get_all_lokasi(skip, limit)
    total = lokasi_service.get_lokasi_count()
    page = (skip // limit) + 1
    
    return paginated_response(
        message="Lokasi berhasil diambil",
        data=data,
        page=page,
        limit=limit,
        total=total
    )
```

### Service dengan Logger

```python
# services/lokasi_service.py
from utils.logger import get_logger

logger = get_logger(__name__)

class LokasiService:
    def create_lokasi(self, data):
        try:
            logger.debug(f"Creating lokasi with data: {data}")
            
            # Validation
            if data.get('jarak_area', 0) < 0:
                logger.warning(f"Invalid jarak_area: {data['jarak_area']}")
                raise HTTPException(400, "Jarak area must be positive")
            
            result = self.repository.create(data)
            logger.info(f"Lokasi created: {result['id_lokasi']}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating lokasi: {str(e)}", exc_info=True)
            raise
```

### Repository dengan Logger

```python
# repositories/lokasi_repository.py
from utils.logger import get_logger

logger = get_logger(__name__)

class LokasiRepository:
    @staticmethod
    def create(data):
        query = "INSERT INTO lokasi (...) VALUES (...) RETURNING *"
        
        try:
            with get_db_connection() as conn:
                cursor = get_db_cursor(conn)
                logger.debug(f"Executing query: {query}")
                cursor.execute(query, data)
                conn.commit()
                result = cursor.fetchone()
                logger.debug(f"Query successful")
                return dict(result)
        except Exception as e:
            logger.error(f"Database error: {str(e)}", exc_info=True)
            raise
```

## 📊 Response Format Standards

### Success Response
```json
{
    "success": true,
    "message": "Operation successful",
    "data": {
        "id": 1,
        "name": "Example"
    }
}
```

### Error Response
```json
{
    "success": false,
    "message": "Error message",
    "data": {
        "error": "Details"
    }
}
```

### Paginated Response
```json
{
    "success": true,
    "message": "Data retrieved",
    "data": [...],
    "meta": {
        "page": 1,
        "limit": 10,
        "total": 50,
        "total_pages": 5
    }
}
```

## 🔍 Logging Levels

- **DEBUG**: Detailed information untuk debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages (tidak error tapi perlu perhatian)
- **ERROR**: Error messages dengan traceback

## 📝 Best Practices

1. **Always use standard response**
   ```python
   # Good
   return success_response("Success", data=result)
   
   # Bad
   return result
   ```

2. **Log important events**
   ```python
   logger.info("User created successfully")
   logger.warning("Invalid input detected")
   logger.error("Database connection failed")
   ```

3. **Use appropriate log levels**
   - INFO: Normal operations
   - WARNING: Unexpected but handled
   - ERROR: Errors that need attention
   - DEBUG: Development/troubleshooting

4. **Include context in logs**
   ```python
   # Good
   logger.info(f"Creating lokasi: {lokasi_name}")
   
   # Bad
   logger.info("Creating")
   ```

## 🧪 Testing

Test dengan curl:
```bash
# Success response
curl http://localhost:8000/api/v1/lokasi/1

# Error response (not found)
curl http://localhost:8000/api/v1/lokasi/999

# Validation error
curl -X POST http://localhost:8000/api/v1/lokasi/ \
  -H "Content-Type: application/json" \
  -d '{"jarak_area": "invalid"}'

# Paginated response
curl "http://localhost:8000/api/v1/lokasi/?skip=0&limit=10"
```

Check logs:
```bash
tail -f backend/logs/app_*.log
```
