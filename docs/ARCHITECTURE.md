# Architecture Documentation

## Overview

AI Voice Reports Bot is built using a layered architecture pattern with clear separation of concerns.

## Architecture Layers

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  (Telegram Bot, API Endpoints)          │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Service Layer                   │
│  (Business Logic)                       │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Repository Layer                │
│  (Data Access)                          │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Database Layer                  │
│  (SQLite/PostgreSQL)                    │
└─────────────────────────────────────────┘
```

## Component Breakdown

### 1. Bot Layer (`src/bot/`)

Handles all Telegram bot interactions.

- **Handlers**: Process different types of messages and commands
  - `common.py`: /start, /help, /cancel
  - `voice.py`: Voice message processing
  - `reports.py`: Report management commands
  - `admin.py`: Admin-only commands

- **Keyboards**: Define inline keyboards for user interaction
- **States**: FSM states for conversation flow
- **Middlewares**: Authentication, logging, etc.

### 2. AI Layer (`src/ai/`)

Manages all AI-related functionality.

- **Transcription**: Voice-to-text using Whisper
- **Validation**: Report validation using LLM
- **Providers**: Abstraction for different AI services
  - OpenAI (GPT + Whisper)
  - Anthropic (Claude)
  - Local LLM (LM Studio/Ollama)

### 3. Database Layer (`src/database/`)

Handles all data persistence.

- **Models**: SQLAlchemy ORM models
  - Employee
  - Department
  - Permission
  - Report
  - ReportSession

- **Repositories**: Data access patterns
  - EmployeeRepository
  - ReportRepository

### 4. Service Layer (`src/services/`)

Contains business logic.

- **ReportService**: Report processing workflow
- **NotificationService**: Reminders and alerts
- **ExportService**: Data export functionality

### 5. API Layer (`src/api/`)

REST API for dashboard and integrations.

- **Routes**: API endpoints
  - `/api/reports`: Report management
  - `/api/employees`: Employee management
  - `/api/analytics`: Statistics and analytics

- **Schemas**: Pydantic models for request/response validation

## Data Flow

### Voice Message Processing

```
1. User sends voice message
   ↓
2. Bot downloads audio
   ↓
3. AI transcribes to text (Whisper)
   ↓
4. LLM validates and extracts data
   ↓
5. If incomplete → Ask clarifying questions
   ↓
6. If complete → Show for confirmation
   ↓
7. User confirms → Save to database
```

### Database Schema

```sql
employees
├── id (PK)
├── full_name
├── messenger_id (unique)
├── messenger_username
└── department_id (FK)

permissions
├── id (PK)
├── employee_id (FK, unique)
├── can_submit_reports
├── can_request_reports
├── can_edit_reports
├── can_export_data
└── is_admin

reports
├── id (PK)
├── employee_id (FK)
├── report_date
├── equipment_number
├── brigade_number
├── work_description
├── transcription
├── structured_data (JSON)
├── status
└── confirmed_at
```

## Design Patterns

### Repository Pattern
Abstracts data access logic from business logic.

### Service Pattern
Encapsulates business logic and orchestrates between layers.

### Dependency Injection
Used in FastAPI routes for database sessions and repositories.

### FSM (Finite State Machine)
Manages conversation states in Telegram bot.

## Configuration

Centralized configuration using Pydantic Settings:
- Environment variables loaded from `.env`
- Type validation
- Default values
- Cached singleton instance

## Logging

Structured logging using Loguru:
- Console output with colors
- File rotation (10 MB chunks)
- Separate error log
- Retention policies

## Testing Strategy

- **Unit Tests**: Individual functions and methods
- **Integration Tests**: Database operations
- **E2E Tests**: Full workflow testing

## Security Considerations

1. **Authentication**: Whitelist of allowed messenger IDs
2. **Authorization**: Role-based access control (RBAC)
3. **Data Privacy**: Optional local AI processing
4. **Input Validation**: Pydantic schemas
5. **SQL Injection**: Prevented by SQLAlchemy ORM

## Scalability

### Current (MVP)
- Single process
- SQLite database
- In-memory FSM storage

### Future
- Multi-process deployment
- PostgreSQL with connection pooling
- Redis for FSM storage
- Horizontal scaling with load balancer

## Performance Optimizations

1. **Async I/O**: All I/O operations are async
2. **Connection Pooling**: Database connection reuse
3. **Caching**: Settings cached as singleton
4. **Batch Processing**: Bulk database operations where possible

## External Dependencies

- **Telegram Bot API**: Message delivery
- **OpenAI API**: Whisper transcription, GPT validation
- **Anthropic API**: Claude validation (optional)
- **Local LLM**: LM Studio/Ollama (optional)
