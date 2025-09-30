# FastAPI Search Service

## Overview

A Python-based REST API backend that provides Google search and YouTube search functionality. Built with FastAPI for high performance and automatic API documentation.

## Features

- 🔍 Google search integration
- 🎥 YouTube video search
- 📚 Automatic API documentation (Swagger/OpenAPI)
- ⚡ High-performance async endpoints
- 🎯 Telugu actor/craft specific search functionality

## API Endpoints

### Health Check

- `GET /` - Returns a simple "Hello World" message
- `GET /hello/{name}` - Personalized greeting

### Search Services

- `POST /find/person/wiki_url` - Find Wikipedia URLs for Telugu actors/crafts
- `POST /find/youtube/videos` - Search YouTube videos with customizable result count

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ramesh-Bojanapu-1011/fast_api.git
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   uvicorn main:app --reload
   ```

   Or alternatively:

   ```bash
   python -m uvicorn main:app --reload
   ```

5. **Access the API**
   - API Base URL: <http://127.0.0.1:8000>
   - Interactive API Documentation: <http://127.0.0.1:8000/docs>
   - Alternative API Documentation: <http://127.0.0.1:8000/redoc>

## API Usage Examples

### Test the API

```bash
curl http://127.0.0.1:8000
```

### Search for YouTube videos

```bash
curl -X POST "http://127.0.0.1:8000/find/youtube/videos" \
     -H "Content-Type: application/json" \
     -d '{"search_text": "FastAPI tutorial", "num_results": 5}'
```

### Find Wikipedia URL for Telugu actor

```bash
curl -X POST "http://127.0.0.1:8000/find/person/wiki_url" \
     -H "Content-Type: application/json" \
     -d '{"name": "Chiranjeevi", "craft": "actor"}'
```

## Testing

### Running Tests

This project includes multiple ways to run tests, from quick basic tests to comprehensive test suites.

#### **Quick Start - Run All Tests**

```bash
# Run all test suites (recommended)
python dev.py test

# Or run individual test suites
python dev.py test-basic     # Basic functional tests
python dev.py test-pytest   # Comprehensive pytest tests
```

#### **1. Basic API Tests (Functional Testing)**

Run the included test script to verify all endpoints are working:

```bash
python test_api.py
```

**What this tests:**

- ✅ Health endpoints (`/` and `/health`)
- ✅ Hello endpoint (`/hello/{name}`)
- ✅ YouTube search endpoint
- ✅ Actor/Wiki search endpoint
- ✅ Basic functionality and response validation

**Sample Output:**

```Sample_Output
🧪 Testing Health Endpoint...
✅ Health Endpoint: PASSED
🧪 Testing YouTube Search...
✅ YouTube Search: PASSED
📊 Test Summary: Passed: 5/5
🎉 All tests passed!
```

#### **2. Comprehensive Pytest Tests (Advanced Testing)**

Run the full test suite with detailed validation:

```bash
python -m pytest test_main.py -v
```

**What this tests:**

- ✅ **17 comprehensive test cases**
- ✅ Input validation and error handling
- ✅ Edge cases and boundary testing
- ✅ Response structure validation
- ✅ HTTP status codes
- ✅ Pydantic model validation
- ✅ API contract compliance

**Sample Output:**

```Sample_Output
test_main.py::TestHealthEndpoints::test_root_endpoint PASSED [5%]
test_main.py::TestSearchEndpoints::test_youtube_search_valid_request PASSED [29%]
...
====== 17 passed in 8.57s =======
```

#### **3. Development Helper Script**

Use the built-in development helper for common tasks:

```bash
# See all available commands
python dev.py help

# Run all tests
python dev.py test

# Start development server
python dev.py serve

# Install dependencies
python dev.py install
```

#### **4. Manual Testing with curl**

Test individual endpoints manually (server must be running):

**Start the server first:**

```bash
python dev.py serve
# or
uvicorn main:app --reload --port 8001
```

**Then test endpoints:**

**Health Check:**

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
```

**Hello Endpoint:**

```bash
curl http://127.0.0.1:8000/hello/YourName
```

**YouTube Search:**

```bash
curl -X POST "http://127.0.0.1:8000/find/youtube/videos" \
     -H "Content-Type: application/json" \
     -d '{"search_text": "Python tutorial", "num_results": 3}'
```

**Actor Search:**

```bash
curl -X POST "http://127.0.0.1:8000/find/person/wiki_url" \
     -H "Content-Type: application/json" \
     -d '{"name": "Chiranjeevi", "craft": "actor"}'
```

#### **5. Interactive Testing (Browser-based)**

Use the automatic API documentation for interactive testing:

1. Start the server: `python dev.py serve`
2. Open browser: <http://127.0.0.1:8000/docs>
3. Try out endpoints directly from the Swagger UI
4. Alternative docs: <http://127.0.0.1:8000/redoc>

#### **6. Test Coverage Summary**

Our test suite covers:

| Test Type | Coverage | Test Count |
|-----------|----------|------------|
| **Functional Tests** | Basic API functionality | 5 tests |
| **Validation Tests** | Input validation & errors | 8 tests |
| **Response Tests** | Response structure | 2 tests |
| **Error Handling** | HTTP errors & edge cases | 4 tests |
| **Integration** | End-to-end workflows | 17 tests |

### Prerequisites for Testing

**For API Tests (test_api.py):** Server must be running

```bash
# Start server on port 8001 (for testing)
uvicorn main:app --reload --port 8001
# Or use the dev helper
python dev.py serve
```

**For Pytest Tests (test_main.py):** No server needed

```bash
# These use FastAPI TestClient - no server required
python -m pytest test_main.py -v
```

## Development

### Project Structure

```Project_Structure
fast_api/
├── main.py              # Main FastAPI application
├── test_api.py          # Basic functional tests
├── test_main.py         # Comprehensive pytest test suite
├── dev.py               # Development helper script
├── requirements.txt     # Python dependencies (including test deps)
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
└── __pycache__/        # Python cache files
```

### Running in Development Mode

The `--reload` flag enables auto-reloading when code changes are detected:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).
