# Testing Quick Reference

## Available Test Commands

### 🚀 **Quick Start**

```bash
python dev.py test          # Run all tests
python dev.py test-basic    # Basic API tests (5 tests)
python dev.py test-pytest  # Comprehensive tests (17 tests)
```

### 📋 **Individual Test Commands**

```bash
# Basic functional tests
python test_api.py

# Comprehensive pytest suite
python -m pytest test_main.py -v

# Run specific test classes
python -m pytest test_main.py::TestHealthEndpoints -v
python -m pytest test_main.py::TestSearchEndpoints -v
```

### 🎯 **Test Coverage**

| Test Suite | Tests | What it covers |
|------------|-------|----------------|
| **test_api.py** | 5 | Basic functionality, endpoint availability |
| **test_main.py** | 17 | Validation, error handling, edge cases |

### 💡 **Development Workflow**

1. **Development**: `python dev.py serve` (start server)
2. **Quick Test**: `python dev.py test-basic` (verify functionality)
3. **Full Test**: `python dev.py test-pytest` (comprehensive validation)
4. **Documentation**: Visit <http://127.0.0.1:8000/docs>

### ✅ **Current Test Status**

- All 22 tests passing
- Zero deprecation warnings
- Pydantic V2 compatible
- Production ready
