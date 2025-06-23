# Backend API Tests

This directory contains comprehensive test coverage for the German Language Portal backend API.

## Test Structure

- `conftest.py` - Pytest configuration and fixtures
- `fixtures.py` - Test data fixtures for German vocabulary
- `test_words.py` - Tests for word-related endpoints
- `test_groups.py` - Tests for group-related endpoints
- `test_study_sessions.py` - Tests for study session endpoints
- `test_dashboard.py` - Tests for dashboard endpoints
- `test_study_activities.py` - Tests for study activity endpoints
- `test_integration.py` - Integration tests for complex workflows

## Running Tests

From the backend-flask directory:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_words.py

# Run specific test
pytest tests/test_words.py::TestWordsAPI::test_get_words_list

# Run tests with detailed output
pytest -v
```

## Test Database

Tests use an in-memory SQLite database that is created fresh for each test function.
The test database includes:
- 5 German words (2 verbs, 2 nouns, 1 adjective)
- 3 word groups
- 2 study activities
- Sample review statistics

## Test Coverage

The tests cover:
- All API endpoints
- Pagination and sorting
- Input validation
- Error handling
- Database integrity
- Complex user workflows
- Edge cases and error conditions