# Test CRUD Endpoints Skill

## Description
This skill creates comprehensive tests for CRUD (Create, Read, Update, Delete) endpoints in the FastAPI backend. It includes unit tests, integration tests, and authentication tests for task management endpoints.

## Purpose
- Generate comprehensive test suite for CRUD endpoints
- Test all HTTP methods (GET, POST, PUT, DELETE) for task operations
- Include authentication and authorization tests
- Validate user isolation (users can only access their own tasks)
- Test error handling and edge cases
- Output complete test files with proper structure
- Follow pytest best practices for FastAPI testing

## Implementation Requirements
- Create test modules for each CRUD operation
- Include fixtures for test database, authenticated users, and test tasks
- Test successful operations and error conditions
- Validate authentication and authorization requirements
- Test user isolation to ensure users can only access their own data
- Include tests for request validation and error responses
- Use pytest fixtures and parametrized tests where appropriate
- Mock external dependencies if needed
- Test pagination, filtering, and sorting if implemented

## Output Format
- Complete test file content with all test cases
- File path: backend/tests/test_tasks_crud.py
- Include proper imports (pytest, FastAPI test client, etc.)
- Add comprehensive test functions with descriptive names
- Include setup and teardown functions as needed
- Add documentation for complex test scenarios
- Provide test configuration files if needed
- Output the full test file as a complete code block

## Additional Considerations
- Implement proper test data cleanup
- Use factory patterns for creating test data
- Consider property-based testing for edge cases
- Include performance tests if needed
- Test concurrent access scenarios
- Implement test coverage requirements
- Follow testing best practices for API endpoints
- Include negative test cases (invalid inputs, unauthorized access)