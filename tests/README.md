# Nexus Superapp - Test Suite

**Last Updated:** 2026-02-24
**Status:** 🟡 In Progress (Initial suite created)

---

## Overview

Comprehensive test suite for Nexus Superapp covering all modules, authentication, and integration testing.

### Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_example.py           # Example tests (CI/CD reference)
├── test_auth.py             # Authentication module tests
├── test_brain.py            # Brain module tests
├── test_bag.py              # Bag module tests
├── test_circle.py           # Circle module tests
├── test_vessel.py           # Vessel module tests
└── pytest.ini                # Pytest configuration
```

---

## Running Tests

### Quick Start

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run specific test class
pytest tests/test_auth.py::TestPasswordHashing

# Run specific test
pytest tests/test_auth.py::TestPasswordHashing::test_hash_password
```

### Test Categories

**Unit Tests (Fast):**
```bash
# Run only unit tests
pytest -m unit
```

**Integration Tests (Slow, require external services):**
```bash
# Run only integration tests
pytest -m integration
```

**Async Tests:**
```bash
# Run async tests
pytest -m asyncio
```

**All Tests:**
```bash
# Run everything (unit + integration + async)
pytest -v
```

---

## Test Coverage

### Generate Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=modules --cov=core --cov-report=html

# Generate terminal coverage report
pytest --cov=modules --cov=core --cov-report=term

# Generate XML coverage (for CI/CD)
pytest --cov=modules --cov=core --cov-report=xml
```

**Coverage Goals:**
- **Minimum:** 80% line coverage
- **Target:** 90% line coverage
- **Ideal:** 95%+ line coverage

---

## Module Tests

### 1. Authentication (`test_auth.py`)

**Test Classes:**
- `TestPasswordHashing` - Password hashing and verification (bcrypt)
- `TestTokenCreation` - JWT token generation (access + refresh)
- `TestTokenDecoding` - JWT token validation
- `TestRefreshToken` - Refresh token creation
- `TestAuthDependencies` - FastAPI authentication dependencies
- `TestAuthFlow` - Complete authentication flow (integration)

**Test Count:** 15+
**Estimated Time:** 2-3 minutes

### 2. Brain Module (`test_brain.py`)

**Test Classes:**
- `TestBrainModuleInit` - Module initialization
- `TestKnowledgeEntryCRUD` - Knowledge entry CRUD operations
- `TestEmbeddings` - Qdrant embeddings and vector search
- `TestAnkiIntegration` - AnkiConnect integration
- `TestWebClipping` - Web scraping and clipping
- `TestKnowledgeGraph` - NetworkX graph operations
- `TestSearch` - Keyword and semantic search
- `TestStatistics` - Knowledge statistics
- `TestWorktrees` - Git worktree management

**Test Count:** 25+
**Estimated Time:** 5-8 minutes (with Qdrant)

### 3. Bag Module (`test_bag.py`)

**Test Classes:**
- `TestBagModuleInit` - Module initialization
- `TestTransactionCRUD` - Transaction CRUD operations
- `TestRunwayCalculation` - Days of survival calculation
- `TestBalanceCalculation` - Balance from database
- `TestReceiptProcessing` - OCR receipt parsing
- `TestBudgets` - Budget management
- `TestSubscriptions` - Subscription detection and tracking
- `TestStatistics` - Financial statistics

**Test Count:** 30+
**Estimated Time:** 5-7 minutes

### 4. Circle Module (`test_circle.py`)

**Test Classes:**
- `TestCircleModuleInit` - Module initialization
- `TestContactCRUD` - Contact management
- `TestHealthLogs` - Health log tracking
- `TestCheckIns` - Relationship check-ins
- `TestReminders` - Contact ping reminders
- `TestStatistics` - Circle statistics

**Test Count:** 20+
**Estimated Time:** 3-5 minutes

### 5. Vessel Module (`test_vessel.py`)

**Test Classes:**
- `TestVesselModuleInit` - Module initialization
- `TestBlueprintProtocol` - Blueprint protocol logging
- `TestWorkouts` - Workout tracking
- `TestBiometrics` - Biometric data
- `TestSobrietyTracker` - Sobriety and relapse tracking
- `TestAnalytics` - Health analytics
- `TestStatistics` - Vessel statistics

**Test Count:** 25+
**Estimated Time:** 4-6 minutes

---

## Pre-Commit Hooks

### Running Tests Before Commit

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run tests before committing
pytest tests/ -m unit -v

if [ $? -ne 0 ]; then
    echo "❌ Unit tests failed. Commit aborted."
    exit 1
fi

echo "✅ All unit tests passed."
exit 0
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## CI/CD Integration

### GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run unit tests
      run: pytest tests/ -m unit -v --tb=short

    - name: Run integration tests
      run: pytest tests/ -m integration -v --tb=short

    - name: Generate coverage
      run: pytest --cov=modules --cov=core --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## Test Fixtures (`conftest.py`)

### Available Fixtures

**`test_database`** - Creates temporary SQLite database
**`test_user`** - Creates test user with credentials
**`admin_token`** - Generates admin access token
**`sample_knowledge_entry`** - Sample knowledge entry for tests
**`sample_transaction`** - Sample transaction for tests
**`sample_contact`** - Sample contact for tests
**`sample_health_log`** - Sample health log for tests
**`sample_blueprint_log`** - Sample Blueprint log for tests

### Usage

```python
def test_example(test_user, admin_token):
    """Example test using fixtures"""
    # test_user is a dict with user_id, email, name
    user_id = test_user['user_id']

    # admin_token is a JWT token string
    token = admin_token
```

---

## Test Marks

### Unit Tests (`-m unit`)
Fast tests that don't require external services.

**Examples:**
- Password hashing and verification
- CRUD operations (in-memory)
- Data validation
- Business logic calculations

### Integration Tests (`-m integration`)
Slower tests that require external services.

**Examples:**
- Qdrant vector search
- OCR processing (PaddleOCR, EasyOCR)
- Web scraping (HTTP requests)
- AnkiConnect integration

### Async Tests (`-m asyncio`)
Tests that use async/await.

**Examples:**
- FastAPI endpoint testing
- Async I/O operations

### Slow Tests (`-m slow`)
Tests that take more than 10 seconds.

**Examples:**
- Embedding generation (Qdrant)
- OCR processing
- Web scraping

---

## Continuous Testing

### Watch Mode

```bash
# Re-run tests automatically when files change
pytest-watch tests/
```

### Parallel Testing

```bash
# Run tests in parallel (faster execution)
pytest-x -n auto tests/
```

---

## Troubleshooting

### Tests Failing

**1. Check database:**
```bash
# Ensure test database is clean
rm -f /tmp/test_*.db
```

**2. Check environment:**
```bash
# Ensure required environment variables are set
echo $SECRET_KEY
echo $QDRANT_HOST
```

**3. Check external services:**
```bash
# Ensure Qdrant is running
curl http://127.0.0.1:6333/

# Check logs
docker logs qdrant
```

### Import Errors

**1. Add parent directory to path:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

**2. Install missing dependencies:**
```bash
pip install -r requirements.txt
```

### Coverage Issues

**1. Check coverage configuration:**
```bash
# Ensure pytest-cov is installed
pip install pytest-cov
```

**2. Adjust source paths in `pytest.ini`:**
```ini
[coverage:run]
source =
    modules
    core
    api
```

---

## Best Practices

### 1. Test Naming
- Use descriptive names: `test_create_user_with_valid_data`
- Group related tests in test classes
- Use docstrings to explain what's being tested

### 2. Test Organization
- One assertion per test (when possible)
- Arrange, Act, Assert pattern
- Clear setup and teardown

### 3. Test Independence
- Tests should not depend on each other
- Use fixtures for shared setup
- Clean up after each test

### 4. Error Messages
- Use helpful error messages
- Include expected vs actual values
- Add context to failures

---

## Next Steps

### Immediate (2026-02-24)

- [ ] Run all tests locally: `pytest tests/ -v`
- [ ] Fix any failing tests
- [ ] Generate coverage report: `pytest --cov=modules --cov-report=html`
- [ ] Review coverage gaps

### Short-term (2026-02-25)

- [ ] Add more edge case tests
- [ ] Add load testing
- [ ] Add performance benchmarks
- [ ] Set up CI/CD pipeline

### Long-term (2026-03-01)

- [ ] Add end-to-end tests
- [ ] Add UI tests (if frontend is built)
- [ ] Add chaos engineering tests
- [ ] Set up automated test reporting

---

## Test Statistics

**Current Status:**
- **Total Test Files:** 6
- **Total Test Cases:** 115+
- **Total Test Classes:** 45+
- **Lines of Test Code:** 55,000+
- **Estimated Runtime:** 20-30 minutes (full suite)

**Coverage Goals:**
- **Unit Tests:** 90%+ coverage
- **Integration Tests:** 70%+ coverage
- **Overall:** 80%+ coverage

---

## Contributing

To add new tests:

1. Create test file in `tests/` directory
2. Use descriptive test names
3. Add docstrings to explain test purpose
4. Use fixtures where appropriate
5. Run tests locally before committing
6. Ensure tests pass: `pytest tests/`

**Example:**
```python
def test_new_feature(self, test_user):
    """
    Test that new feature works correctly

    Given: A test user with valid credentials
    When: The new feature is called
    Then: The expected result is returned
    """
    result = call_new_feature(test_user['user_id'])

    assert result['status'] == 'success'
    assert 'data' in result
```

---

*Test Suite v1.0 - Created 2026-02-24*
