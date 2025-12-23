# Integration Tests

Integration tests require a PostgreSQL database to be running.

## Setup

For integration tests to work, you need:

1. PostgreSQL running (locally or in Docker)
2. A test database created: `test_microblog`
3. Proper credentials configured

## Skip Integration Tests

If you don't have PostgreSQL set up, you can skip integration tests:

```bash
pytest tests/unit  # Only run unit tests
```

Or mark integration tests to be skipped when DB is not available.

