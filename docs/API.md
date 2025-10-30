# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, API is open (no authentication). Authentication will be added in future versions.

## Endpoints

### Health Check

```http
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

---

### Reports

#### Get All Reports

```http
GET /api/reports?limit=100&offset=0&start_date=2025-01-01
```

Query Parameters:
- `limit` (optional): Number of records (default: 100)
- `offset` (optional): Pagination offset (default: 0)
- `start_date` (optional): Filter by start date (YYYY-MM-DD)

Response:
```json
[
  {
    "id": 1,
    "employee_id": 1,
    "report_date": "2025-10-30",
    "equipment_number": "K-101",
    "brigade_number": "B-3",
    "work_description": "Проверка топливной системы",
    "transcription": "...",
    "structured_data": {...},
    "status": "confirmed",
    "confirmed_at": "2025-10-30T10:00:00Z",
    "created_at": "2025-10-30T09:55:00Z",
    "updated_at": "2025-10-30T10:00:00Z"
  }
]
```

#### Get Report by ID

```http
GET /api/reports/{report_id}
```

Response: Same as single report object above

#### Create Report

```http
POST /api/reports
Content-Type: application/json

{
  "employee_id": 1,
  "report_date": "2025-10-30",
  "equipment_number": "K-101",
  "brigade_number": "B-3",
  "work_description": "Описание работ",
  "transcription": "Транскрипция",
  "structured_data": {}
}
```

Response: Created report object (201 Created)

#### Delete Report

```http
DELETE /api/reports/{report_id}
```

Response: 204 No Content

---

### Employees

#### Get All Employees

```http
GET /api/employees?limit=100&offset=0
```

Response:
```json
[
  {
    "id": 1,
    "full_name": "Иван Иванов",
    "messenger_id": "123456789",
    "messenger_username": "ivan_ivanov",
    "department_id": 1,
    "created_at": "2025-10-30T09:00:00Z",
    "updated_at": "2025-10-30T09:00:00Z"
  }
]
```

#### Get Employee by ID

```http
GET /api/employees/{employee_id}
```

#### Get Employee by Messenger ID

```http
GET /api/employees/messenger/{messenger_id}
```

---

### Analytics

#### Get Overall Statistics

```http
GET /api/analytics/stats
```

Response:
```json
{
  "total_reports": 150,
  "total_employees": 25,
  "reports_today": 10,
  "reports_this_week": 45,
  "reports_this_month": 120
}
```

#### Get Employee Statistics

```http
GET /api/analytics/employee/{employee_id}/stats
```

Response:
```json
{
  "employee_id": 1,
  "total_reports": 25,
  "reports_this_month": 15,
  "average_reports_per_week": 3.5
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Rate Limiting

Currently no rate limiting. Will be added in future versions.

## Versioning

API is currently v1 (implicit). Future versions will use explicit versioning:
- `/api/v1/reports`
- `/api/v2/reports`
