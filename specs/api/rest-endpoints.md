# REST API Endpoints Specification: Todo Backend

## Overview
This document specifies the REST API endpoints for the Todo application backend. The backend is built with Python FastAPI and SQLModel, and integrates with Better Auth for authentication. All protected endpoints require JWT authentication in the Authorization header.

## Base URL
- Development: `http://localhost:8000`
- Production: To be determined

## Authentication
- All protected endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer <jwt-token>`
- Tokens are issued by Better Auth upon successful login
- User identity is verified through JWT decoding using the shared secret
- Path parameter `{user_id}` must match the authenticated user's ID (403 Forbidden if mismatch)

## Common Response Formats

### Success Responses
- Standard 200 OK for successful GET, PUT, PATCH requests
- 201 Created for successful POST requests
- 204 No Content for successful DELETE requests

### Error Responses
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User attempting to access resources they don't own, or user_id mismatch
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation error in request body
- 500 Internal Server Error: Unexpected server error

## Endpoints

### Task Management

#### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for the authenticated user
**Authentication**: Required (JWT)
**Parameters**:
- Path: `user_id` (integer) - authenticated user's ID
- Query: `status` (string, optional) - filter by status: `all`, `pending`, `completed` (default: `all`)
- Query: `sort` (string, optional) - sort by: `created`, `title`, `due_date` (default: `created`)

**Response**:
- 200 OK: Array of task objects
```json
[
  {
    "id": 1,
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "due_date": "2023-12-31T10:00:00Z",
    "created_at": "2023-11-01T10:00:00Z",
    "updated_at": "2023-11-01T10:00:00Z"
  }
]
```

#### POST /api/{user_id}/tasks
**Description**: Create a new task for the authenticated user
**Authentication**: Required (JWT)
**Parameters**:
- Path: `user_id` (integer) - authenticated user's ID

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Task description (optional)",
  "due_date": "2023-12-31T10:00:00Z" (optional)
}
```

**Validation**:
- `title`: Required string, 1-200 characters
- `description`: Optional string, ≤1000 characters
- `due_date`: Optional datetime string in ISO format

**Response**:
- 201 Created: Created task object
```json
{
  "id": 1,
  "title": "New task title",
  "description": "Task description (optional)",
  "completed": false,
  "due_date": "2023-12-31T10:00:00Z",
  "created_at": "2023-11-01T10:00:00Z",
  "updated_at": "2023-11-01T10:00:00Z"
}
```

#### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific task for the authenticated user
**Authentication**: Required (JWT)
**Parameters**:
- Path: `user_id` (integer) - authenticated user's ID
- Path: `id` (integer) - task ID

**Response**:
- 200 OK: Task object
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Task description",
  "completed": false,
  "due_date": "2023-12-31T10:00:00Z",
  "created_at": "2023-11-01T10:00:00Z",
  "updated_at": "2023-11-01T10:00:00Z"
}
```

#### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task for the authenticated user
**Authentication**: Required (JWT)
**Parameters**:
- Path: `user_id` (integer) - authenticated user's ID
- Path: `id` (integer) - task ID

**Request Body** (all fields optional):
```json
{
  "title": "Updated task title (optional)",
  "description": "Updated task description (optional)",
  "completed": true,
  "due_date": "2023-12-31T10:00:00Z" (optional)
}
```

**Response**:
- 200 OK: Updated task object
```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true,
  "due_date": "2023-12-31T10:00:00Z",
  "created_at": "2023-11-01T10:00:00Z",
  "updated_at": "2023-11-02T10:00:00Z"
}
```

#### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task for the authenticated user
**Authentication**: Required (JWT)
**Parameters**:
- Path: `user_id` (integer) - authenticated user's ID
- Path: `id` (integer) - task ID

**Response**:
- 204 No Content: Successfully deleted

#### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle the completion status of a specific task
**Authentication**: Required (JWT)
**Parameters**:
- Path: `user_id` (integer) - authenticated user's ID
- Path: `id` (integer) - task ID

**Request Body**:
```json
{
  "completed": true
}
```

**Response**:
- 200 OK: Updated task object
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Task description",
  "completed": true,
  "due_date": "2023-12-31T10:00:00Z",
  "created_at": "2023-11-01T10:00:00Z",
  "updated_at": "2023-11-02T10:00:00Z"
}
```

## Better Auth Integration Endpoints
These endpoints are handled automatically by Better Auth and mounted in the main application:
- POST /api/auth/signin
- POST /api/auth/signup
- GET /api/auth/session
- POST /api/auth/signout
- And other auth-related endpoints

## Security Considerations
- All endpoints validate JWT tokens against the shared secret
- User ID in path must match the authenticated user's ID
- Input validation using Pydantic models
- No data leakage between users
- Proper error handling without revealing sensitive information