# Tasks CRUD Routes FastAPI Skill

## Description
This skill implements full CRUD (Create, Read, Update, Delete) routes for task management in FastAPI with proper user isolation. It ensures users can only access and modify their own tasks.

## Purpose
- Implement full CRUD operations for tasks at /api/tasks or /api/{user_id}/tasks endpoints
- Ensure proper user isolation so users can only access their own tasks
- Follow REST API conventions and FastAPI best practices
- Include proper authentication and authorization
- Handle validation and error responses appropriately
- Output complete file with path: backend/app/api/v1/tasks.py

## Implementation Requirements
- Implement GET /api/tasks to list user's tasks with pagination
- Implement GET /api/tasks/{id} to retrieve a specific task
- Implement POST /api/tasks to create a new task
- Implement PUT /api/tasks/{id} to update an existing task
- Implement DELETE /api/tasks/{id} to delete a task
- Ensure user isolation by validating task ownership
- Use authentication dependency to get current user
- Apply proper validation using Pydantic models
- Return appropriate HTTP status codes
- Include proper error handling with HTTPException
- Add proper type hints and documentation

## Output Format
- Complete file content with all CRUD route implementations
- File path: backend/app/api/v1/tasks.py
- Include proper imports (FastAPI, Depends, HTTPException, etc.)
- Include request/response models
- Add comprehensive documentation for each endpoint
- Include example usage and error responses
- Add note about router inclusion in main.py

## Additional Considerations
- Implement proper pagination for task listings
- Include filtering and sorting options if needed
- Add rate limiting if necessary
- Ensure proper database session management
- Include transaction handling where appropriate
- Follow security best practices for user isolation
- Add logging for debugging and monitoring
- Consider soft deletes if needed for data retention