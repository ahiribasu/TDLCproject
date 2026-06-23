# Tokenization API

Small FastAPI application that tokenizes input text and returns a list of tokens plus a SHA-256 checksum of the original text.

## Files
- `main.py` - FastAPI application with endpoints:
  - `GET /`         - welcome message (customized)
  - `POST /generate` - accept JSON body `{ "text": "..." }` and return tokens + checksum
- `tests/test_generate.py` - pytest-based tests using FastAPI's TestClient

## Requirements
- Python 3.8+
- Install dependencies:
  pip install fastapi uvicorn pydantic pytest

## Run the app (development)
Start the uvicorn server:

```bash
uvicorn main:app --reload --port 8000
