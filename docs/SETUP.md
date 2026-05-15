# Backend Setup Guide

## Prerequisites
- Python 3.9+
- pip (Python package manager)
- Virtual environment tool (venv or conda)

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/StudentFaizan7426/legal-recon.git
cd legal-recon/backend
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit .env with your settings
```

### 5. Run Application
```bash
python main.py
```

Application will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Testing the API

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Sample FIR Preprocessing
```bash
curl -X POST http://localhost:8000/api/v1/fir/preprocess \
  -H "Content-Type: application/json" \
  -d '{
    "fir_text": "یہ ایک نمونہ اردو متن ہے",
    "fir_id": "FIR-2024-001"
  }'
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # App entry point
│   ├── config.py               # Configuration
│   ├── api/
│   │   ├── router.py           # Main router
│   │   └── endpoints/          # API endpoints
│   ├── core/
│   │   ├── logging.py          # Logging setup
│   │   └── errors.py           # Custom exceptions
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   └── services/               # Business logic
│       ├── preprocessing.py
│       ├── ner.py
│       ├── ppc_mapper.py
│       └── timeline.py
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
├── Dockerfile                 # Docker configuration
└── .gitignore
```

## Common Issues

### Port Already in Use
```bash
# Change port in .env
PORT=8001
```

### Module Not Found
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

1. Implement NLP preprocessing in `services/preprocessing.py`
2. Implement entity extraction in `services/ner.py`
3. Implement PPC mapping in `services/ppc_mapper.py`
4. Implement timeline generation in `services/timeline.py`
5. Add tests in `tests/` directory

## Support

For issues, create a GitHub issue or contact the team.
