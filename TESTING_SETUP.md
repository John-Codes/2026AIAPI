# Real Endpoint Testing Setup

## Overview

This project now uses **REAL ENDPOINT TESTS** instead of mock tests. All tests make actual HTTP requests to a running FastAPI server on `localhost:8000`.

**NO MOCK TESTS ARE EVER ALLOWED** - This is a strict requirement for all testing in this project.

## Prerequisites

### 1. Python 3.8+
```bash
python --version
```

### 2. Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. OpenRouter API Key
Get your API key from: https://openrouter.ai/keys

Set the environment variable:
```bash
export OpenRouter=your_actual_api_key_here
```

Or copy `.env.example` to `.env` and configure it:
```bash
cp .env.example .env
# Edit .env file with your API key
```

## Quick Start

### 1. Setup Environment
```bash
python test_setup.py
```

### 2. Start the FastAPI Server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 3. Run Tests
```bash
# Option 1: Use the test runner (recommended)
python run_tests.py

# Option 2: Run pytest directly
pytest test_real_endpoints.py -v

# Option 3: Run specific test
pytest test_real_endpoints.py::TestRealEndpoints::test_heartbeat_endpoint -v
```

## Test Files

### `test_real_endpoints.py`
Main test file containing all real endpoint tests:
- **`test_heartbeat_endpoint`** - Tests server health check
- **`test_generate_endpoint_text_only`** - Tests text generation
- **`test_generate_endpoint_with_invalid_api_key`** - Tests error handling
- **`test_generate_endpoint_missing_text_field`** - Tests validation
- **`test_generate_endpoint_with_image_url`** - Tests multimodal requests
- **`test_server_connection_error`** - Tests connection handling
- **`test_timeout_handling`** - Tests timeout scenarios

### `test_setup.py`
Setup and configuration helper:
- Checks Python version compatibility
- Verifies required dependencies
- Validates OpenRouter API key configuration
- Creates configuration files

### `run_tests.py`
Test runner script that runs prerequisite checks before executing tests.

### `.env.example`
Environment variable template. Copy to `.env` and configure your API key.

## Test Endpoints

### Health Check (`/heartbeat`)
```bash
curl -X GET "http://localhost:8000/heartbeat" -H "accept: application/json"
```

### Generate (`/generate`)
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, tell me about AI",
    "api_key": "your_api_key_here",
    "model_name": "z-ai/glm-4.5-air:free"
  }'
```

## Test Configuration

### Environment Variables
- `OpenRouter` - Your OpenRouter API key (required)
- `Model_Name` - Model name (optional, defaults to "z-ai/glm-4.5-air:free")
- `HOST` - Server host (optional, defaults to "0.0.0.0")
- `PORT` - Server port (optional, defaults to "8000")

### Test Configuration in Code
```python
# Base URL for all tests
BASE_URL = "http://localhost:8000"

# Test timeout
TIMEOUT = 30.0

# API key from environment
TEST_API_KEY = os.getenv("OpenRouter", "sk-or-xxxx")
```

## Running Tests in CI/CD

For automated testing, ensure the server is running and environment variables are set:

```bash
# Start server in background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Wait for server to be ready
python -c "import time; time.sleep(5); import httpx; httpx.get('http://localhost:8000/heartbeat')"

# Run tests
pytest test_real_endpoints.py -v --tb=short
```

## Troubleshooting

### Server Not Running
```
❌ FastAPI server is not running on localhost:8000
   Please start it with: uvicorn app:app --host 0.0.0.0 --port 8000
```

**Solution:**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Missing API Key
```
⚠️  OpenRouter API key not configured or using default
   Set your API key: export OpenRouter=your_actual_api_key_here
```

**Solution:**
```bash
export OpenRouter=your_actual_api_key_here
# or
cp .env.example .env
# Edit .env with your API key
```

### Missing Dependencies
```
❌ httpx is missing
❌ pytest is missing
```

**Solution:**
```bash
pip install -r requirements.txt
```

### Connection Timeouts
If tests timeout, check:
1. Server is running on correct port
2. Network connectivity
3. Firewall settings

## Test Coverage

The real endpoint tests cover:

✅ **Health Check Endpoint**
- Server availability
- Response format validation
- Status code verification

✅ **Generate Endpoint**
- Text-only requests
- Image URL requests
- API key validation
- Error handling
- Input validation
- Timeout handling

✅ **Error Scenarios**
- Invalid API keys
- Missing required fields
- Connection failures
- Server unavailability

✅ **Integration Testing**
- Real OpenRouter API calls
- Multimodal requests
- Environment variable handling

## Important Notes

1. **NO MOCK TESTS EVER** - All tests must make real HTTP requests
2. **Server Must Be Running** - Tests require a running FastAPI server
3. **Valid API Key Required** - Generate endpoint tests need a real OpenRouter API key
4. **Network Access** - Tests require internet access for OpenRouter API calls
5. **Environment Variables** - Proper configuration is required for successful tests

## Development Guidelines

When adding new tests:

1. **Use Real HTTP Requests** - Always use `httpx` for real endpoint calls
2. **Test Error Scenarios** - Include tests for failure cases
3. **Validate Responses** - Check status codes and response structure
4. **Handle Timeouts** - Include timeout handling in network requests
5. **Document Tests** - Add clear docstrings explaining test purpose
6. **Skip When Appropriate** - Use `pytest.skip()` for missing prerequisites

Example test structure:
```python
def test_new_endpoint(self, client, is_server_running):
    """Test new endpoint with real HTTP request"""
    if not is_server_running:
        pytest.skip("FastAPI server is not running")
    
    # Make real HTTP request
    response = client.get("/new-endpoint")
    
    # Validate response
    assert response.status_code == 200
    assert "expected_field" in response.json()