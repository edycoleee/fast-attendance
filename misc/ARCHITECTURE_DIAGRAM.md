# Clean Architecture - Flow Diagram

## 📊 Request Flow

```
HTTP Request
    ↓
┌─────────────────────────────────────────────────┐
│  API Layer (api/v1/endpoints/lokasi.py)        │
│  - Route handlers                                │
│  - Input validation (Pydantic)                   │
│  - HTTP response formatting                      │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  Service Layer (services/lokasi_service.py)     │
│  - Business logic                                │
│  - Validations                                   │
│  - Error handling                                │
│  - Orchestration                                 │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  Repository Layer (repositories/lokasi_repo.py) │
│  - Raw SQL queries                               │
│  - Database operations                           │
│  - Query optimization                            │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  Database (PostgreSQL)                          │
│  - Data storage                                  │
│  - Tables: lokasi, pegawai, etc                 │
└─────────────────────────────────────────────────┘
```

## 🎯 Example: Create Lokasi Flow

### 1. API Layer receives request
```python
# api/v1/endpoints/lokasi.py

@router.post("/")
def create_lokasi(lokasi: LokasiCreate):
    # Input validated by Pydantic automatically
    data = lokasi.model_dump()
    
    # Call service layer
    result = lokasi_service.create_lokasi(data)
    
    # Return response
    return result
```

### 2. Service Layer processes business logic
```python
# services/lokasi_service.py

def create_lokasi(self, data: Dict[str, Any]):
    # Business validation
    if data.get('jarak_area') < 0:
        raise HTTPException(400, "Jarak area must be positive")
    
    # Call repository
    result = self.repository.create(data)
    
    if not result:
        raise HTTPException(500, "Failed to create lokasi")
    
    return result
```

### 3. Repository Layer executes SQL
```python
# repositories/lokasi_repository.py

@staticmethod
def create(data: Dict[str, Any]):
    query = """
        INSERT INTO lokasi (nama_lokasi, lat, long, jarak_area)
        VALUES (%(nama_lokasi)s, %(lat)s, %(long)s, %(jarak_area)s)
        RETURNING id_lokasi, nama_lokasi, lat, long, jarak_area
    """
    
    with get_db_connection() as conn:
        cursor = get_db_cursor(conn)
        cursor.execute(query, data)
        conn.commit()
        return dict(cursor.fetchone())
```

## 🔄 Data Flow

```
Client Request
    ↓
┌──────────────────┐
│  LokasiCreate    │  ← Pydantic Schema (Validation)
│  (Pydantic)      │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Dict[str, Any]  │  ← Plain Python Dict
└────────┬─────────┘
         ↓
┌──────────────────┐
│  SQL Query       │  ← Raw SQL with params
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Database        │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  RealDictRow     │  ← psycopg2 result
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Dict[str, Any]  │  ← Converted to dict
└────────┬─────────┘
         ↓
┌──────────────────┐
│  LokasiResponse  │  ← Pydantic Response Model
│  (Pydantic)      │
└────────┬─────────┘
         ↓
    JSON Response
```

## 📂 File Organization

```
backend/
│
├── api/                     ← Presentation Layer
│   └── v1/
│       ├── endpoints/       ← Route handlers
│       │   └── lokasi.py
│       ├── router.py        ← Combine all endpoints
│       └── schemas.py       ← Request/Response models
│
├── services/                ← Business Logic Layer
│   └── lokasi_service.py    ← Business rules
│
├── repositories/            ← Data Access Layer
│   └── lokasi_repository.py ← SQL queries
│
├── config/                  ← Configuration
│   ├── settings.py          ← Environment config
│   └── database.py          ← DB connections
│
├── utils/                   ← Utilities
│   └── db.py                ← Helper functions
│
└── main.py                  ← FastAPI app
```

## 🎨 Dependency Direction

```
         ┌──────────────┐
         │  API Layer   │
         └──────┬───────┘
                │ depends on
                ↓
         ┌──────────────┐
         │ Service Layer│
         └──────┬───────┘
                │ depends on
                ↓
         ┌──────────────┐
         │Repository Lyr│
         └──────┬───────┘
                │ depends on
                ↓
         ┌──────────────┐
         │   Database   │
         └──────────────┘
```

**Important**: Dependencies always point INWARD
- API knows about Service
- Service knows about Repository
- Repository knows about Database
- Database knows NOTHING about upper layers

## 🔐 Principles

### 1. Single Responsibility Principle
Each layer has ONE job:
- **API**: Handle HTTP
- **Service**: Business logic
- **Repository**: Data access

### 2. Dependency Inversion
- Depend on abstractions, not concretions
- Inner layers don't know about outer layers

### 3. Separation of Concerns
- Each file has a specific purpose
- Easy to find and modify code

### 4. Testability
```python
# Test repository independently
def test_lokasi_repository():
    repo = LokasiRepository()
    result = repo.find_all()
    assert isinstance(result, list)

# Test service independently
def test_lokasi_service():
    service = LokasiService()
    # Can mock repository
    result = service.get_all_lokasi()
    assert result is not None
```

## 🚀 Benefits

✅ **Maintainable**: Easy to find and fix bugs  
✅ **Testable**: Each layer can be tested independently  
✅ **Scalable**: Easy to add new features  
✅ **Flexible**: Easy to change database or framework  
✅ **Clear**: Code organization is intuitive  
✅ **Professional**: Industry best practices  
