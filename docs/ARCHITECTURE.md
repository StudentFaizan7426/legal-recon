# Legal Recon Backend Architecture

## Overview

Legal Recon is an AI-Based Legal Intelligence System that processes Urdu FIRs (First Information Reports) to extract structured legal insights, PPC suggestions, and scene reconstruction.

## System Architecture

### 1. **API Layer** (`app/api/`)
FastAPI-based REST API with modular endpoints

#### Endpoints:
- `POST /api/v1/fir/preprocess` - Preprocess Urdu text
- `POST /api/v1/fir/extract-entities` - Extract named entities
- `POST /api/v1/fir/map-ppc` - Map to PPC sections
- `POST /api/v1/fir/generate-timeline` - Generate event timeline
- `POST /api/v1/analysis/analyze-fir` - Complete FIR analysis
- `GET /api/v1/health` - Health check
- `GET /api/v1/ready` - Readiness check

### 2. **Service Layer** (`app/services/`)
Business logic and NLP pipeline

#### Services:
- **PreprocessingService**: Urdu text cleaning, normalization, tokenization
- **NERService**: Named Entity Recognition for persons, locations, crimes
- **PPCMappingService**: Maps crimes to Penal Code sections
- **TimelineService**: Reconstructs chronological event sequence

### 3. **Data Models** (`app/models/`)
Pydantic schemas for request/response validation

#### Schema Categories:
- FIR Processing: Request/response models for each service
- Entity Models: Person, location, crime, organization, evidence
- PPC Models: Penal Code section suggestions
- Timeline Models: Event and temporal relationship models
- Analysis Models: Comprehensive analysis response

### 4. **Core Module** (`app/core/`)
Cross-cutting concerns

- **config.py**: Environment-based configuration using Pydantic
- **logging.py**: Structured logging setup
- **errors.py**: Custom exception hierarchy

### 5. **Middleware**
- CORS middleware for frontend integration
- Request/response logging
- Exception handling

## Data Flow

```
Client Request
    ↓
FastAPI Router
    ↓
Request Validation (Pydantic)
    ↓
Service Layer (NLP Pipeline)
    ├─→ PreprocessingService
    ├─→ NERService
    ├─→ PPCMappingService
    └─→ TimelineService
    ↓
Response Model Validation
    ↓
Client Response
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Async Runtime | Uvicorn |
| Validation | Pydantic |
| NLP | spaCy, Transformers |
| Text Processing | NLTK, Urdu-NLP |
| Database | SQLAlchemy (future) |
| Testing | pytest |

## Development Phases

### Phase 1: Foundation (✅ Current)
- [x] FastAPI structure
- [x] Configuration management
- [x] Pydantic schemas
- [x] Service layer skeleton
- [x] API endpoints
- [x] Error handling

### Phase 2: NLP Core (In Progress)
- [ ] Urdu text preprocessing
- [ ] Entity extraction (NER)
- [ ] Language detection
- [ ] Tokenization

### Phase 3: Business Logic
- [ ] PPC section database
- [ ] Intelligent PPC mapping
- [ ] Timeline reconstruction
- [ ] Relationship extraction

### Phase 4: Integration & Polish
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Documentation
- [ ] Docker deployment

## Running the Application

### Development
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Production
```bash
unicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker build -t legal-recon:latest .
docker run -p 8000:8000 legal-recon:latest
```

## API Documentation

Available at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- OpenAPI JSON: `http://localhost:8000/api/openapi.json`

## Configuration

See `.env.example` for all available environment variables.

## Team Responsibilities

### Lead + Backend + AI Core (You)
- NLP pipeline development
- PPC mapping logic
- API development
- Architecture decisions

### Frontend + Visualization
- React/Flutter UI
- Graph visualization
- Map integration
- Dashboard

### Data + Integration + Testing
- Dataset collection
- Data cleaning
- Testing modules
- Integration support
- PDF report generation
