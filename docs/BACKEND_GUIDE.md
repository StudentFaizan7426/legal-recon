# Backend Development Guide

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application factory
│   ├── config.py               # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoint implementations
│   ├── core/
│   │   ├── __init__.py
│   │   ├── logging.py          # Structured logging configuration
│   │   ├── errors.py           # Custom exceptions
│   │   └── config.py           # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic request/response models
│   └── services/
│       ├── __init__.py
│       ├── preprocessing.py    # Urdu text preprocessing
│       ├── ner.py             # Named Entity Recognition
│       ├── ppc_mapper.py       # PPC section mapping
│       └── timeline.py         # Timeline generation
├── main.py                     # Entry point for development
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .env.example               # Environment variables template
└── .dockerignore
```

## Setup Instructions

### 1. Local Development

#### Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Create environment file
```bash
cp .env.example .env
# Edit .env with your settings
```

#### Run application
```bash
python main.py
```

The application will start at `http://localhost:8000`

#### Access documentation
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### 2. Docker Deployment

#### Build Docker image
```bash
docker build -t legal-recon:latest .
```

#### Run container
```bash
docker run -p 8000:8000 \
  -e APP_NAME="Legal Recon" \
  -e DEBUG="False" \
  -e ENVIRONMENT="production" \
  legal-recon:latest
```

#### Docker Compose (Optional)
```bash
docker-compose up -d
```

## API Endpoints

### Health & Status

#### Health Check
```
GET /api/v1/health
```

#### Readiness Check
```
GET /api/v1/ready
```

### Text Processing

#### Preprocess Urdu FIR Text
```
POST /api/v1/preprocess

Request:
{
  "fir_text": "Urdu FIR text here",
  "fir_id": "FIR-2024-001"
}

Response:
{
  "original_text": "...",
  "preprocessed_text": "...",
  "text_length": 1000,
  "token_count": 150,
  "language_detected": "urdu"
}
```

### Entity Extraction

#### Extract Entities from FIR
```
POST /api/v1/entities/extract

Request:
{
  "fir_text": "Urdu FIR text",
  "fir_id": "FIR-2024-001"
}

Response:
{
  "fir_id": "FIR-2024-001",
  "entities": [
    {
      "text": "Muhammad Ali",
      "entity_type": "PERSON",
      "confidence": 0.95,
      "start_pos": 10,
      "end_pos": 22
    }
  ],
  "entity_count": 5,
  "extraction_confidence": 0.92
}
```

### PPC Mapping

#### Map FIR to PPC Sections
```
POST /api/v1/ppc/map

Request:
{
  "fir_text": "Crime description",
  "entities": [...],
  "fir_id": "FIR-2024-001"
}

Response:
{
  "fir_id": "FIR-2024-001",
  "suggested_sections": [
    {
      "section_number": "302",
      "section_title": "Punishment for murder",
      "punishment": "Death or life imprisonment",
      "relevance_score": 0.95
    }
  ],
  "primary_section": {...},
  "secondary_sections": [...],
  "total_matching_sections": 3
}
```

### Timeline Generation

#### Generate Event Timeline
```
POST /api/v1/timeline/generate

Request:
{
  "fir_text": "Crime description",
  "fir_id": "FIR-2024-001"
}

Response:
{
  "fir_id": "FIR-2024-001",
  "timeline_events": [
    {
      "event_id": "event_1",
      "event_description": "Crime occurred",
      "timestamp": "2024-01-15T10:30:00",
      "location": "Model Town",
      "entities_involved": ["Ahmed", "Hassan"],
      "confidence": 0.88
    }
  ],
  "event_sequence": ["event_1", "event_2", "event_3"],
  "temporal_coverage_days": 5
}
```

### Comprehensive Analysis

#### Complete FIR Analysis
```
POST /api/v1/analyze

Request:
{
  "fir_text": "Complete FIR text",
  "fir_id": "FIR-2024-001"
}

Response:
{
  "fir_id": "FIR-2024-001",
  "preprocessing": {...},
  "entities": {...},
  "ppc_mapping": {...},
  "timeline": {...},
  "overall_confidence": 0.92
}
```

## Configuration

All configuration is managed through environment variables in `.env` file.

### Key Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Legal Recon |
| `APP_VERSION` | Version number | 0.1.0 |
| `DEBUG` | Debug mode | False |
| `ENVIRONMENT` | Environment type | development |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `LOG_LEVEL` | Logging level | INFO |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000 |

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Implement feature
- Add tests
- Update documentation

### 3. Run Tests
```bash
pytest tests/
pytest --cov=app tests/  # With coverage
```

### 4. Code Quality
```bash
# Format code
black app/

# Check style
flake8 app/
isort app/

# Type checking
mypy app/
```

### 5. Commit and Push
```bash
git add .
git commit -m "feat: description of your feature"
git push origin feature/your-feature-name
```

## Service Architecture

### 1. PreprocessingService
- **Responsibility**: Clean and normalize Urdu text
- **Methods**:
  - `preprocess()`: Main preprocessing pipeline
  - `_clean_text()`: Remove noise
  - `_normalize_unicode()`: Unicode normalization
  - `_normalize_urdu_characters()`: Urdu-specific normalization
  - `_tokenize()`: Split into tokens

### 2. NERService
- **Responsibility**: Extract named entities
- **Entities**: PERSON, LOCATION, CRIME, ORGANIZATION, EVIDENCE, TIME
- **Methods**:
  - `extract_entities()`: Main extraction pipeline
  - `_extract_by_keywords()`: Keyword-based extraction
  - `_extract_by_patterns()`: Regex pattern extraction
  - `_extract_by_context()`: Contextual extraction

### 3. PPCMappingService
- **Responsibility**: Map crimes to Penal Code sections
- **Methods**:
  - `map_ppc_sections()`: Main mapping logic
  - `_match_sections()`: Match text to PPC database

### 4. TimelineService
- **Responsibility**: Reconstruct event sequence
- **Methods**:
  - `generate_timeline()`: Main timeline generation
  - `_extract_events()`: Extract individual events
  - `_extract_temporal_info()`: Extract time information
  - `_sort_chronologically()`: Sort events by time

## Error Handling

The application uses custom exceptions for different scenarios:

- `PreprocessingError`: Text preprocessing failures
- `EntityExtractionError`: Entity extraction failures
- `PPCMappingError`: PPC mapping failures
- `TimelineGenerationError`: Timeline generation failures
- `ValidationError`: Input validation failures
- `ModelNotFoundError`: Missing NLP models

All exceptions are handled consistently with proper HTTP status codes and error details.

## Performance Optimization

### Caching
- Configuration loaded once with `@lru_cache()`
- Service instances reused globally

### Async Processing
- FastAPI with async/await support
- Non-blocking I/O operations

### Resource Limits
- `MAX_TEXT_LENGTH`: 50000 characters
- `PROCESSING_TIMEOUT`: 300 seconds

## Testing

### Unit Tests
```bash
pytest tests/services/
```

### Integration Tests
```bash
pytest tests/integration/
```

### Test Coverage
```bash
pytest --cov=app --cov-report=html tests/
```

## Logging

Structured JSON logging with:
- **Console**: Real-time monitoring
- **File**: Persistent logs in `logs/app.log`
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

Example log output:
```json
{
  "timestamp": 1234567890.123,
  "level": "INFO",
  "logger": "app.services.preprocessing",
  "message": "✓ Successfully preprocessed text",
  "module": "preprocessing",
  "function": "preprocess"
}
```

## Monitoring

### Health Checks
- `/api/v1/health`: Basic health status
- `/api/v1/ready`: Service readiness

### Metrics
- Processing time recorded in all responses
- Confidence scores for all operations
- Entity extraction counts and quality

## Troubleshooting

### Common Issues

#### 1. Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

#### 2. Urdu Text Encoding Issues
```python
# Ensure UTF-8 encoding in files
# Add to Python scripts:
# -*- coding: utf-8 -*-
```

#### 3. NLP Model Loading Errors
```bash
# Verify model paths in .env
ls -la models/
```

#### 4. CORS Errors
```python
# Check CORS_ORIGINS in .env
# Add frontend URL if missing
```

## Best Practices

1. **Code Style**: Follow PEP 8 with Black formatter
2. **Type Hints**: Use type hints for all functions
3. **Documentation**: Add docstrings to all methods
4. **Logging**: Use appropriate log levels
5. **Error Handling**: Catch and handle specific exceptions
6. **Testing**: Write tests for new features
7. **Configuration**: Use environment variables

## Contributing Guidelines

1. Create feature branch
2. Implement feature with tests
3. Ensure all tests pass
4. Add/update documentation
5. Commit with clear messages
6. Push and create PR

## Support

For issues or questions:
1. Check documentation
2. Review logs
3. Create GitHub issue with details
4. Provide reproducible steps

