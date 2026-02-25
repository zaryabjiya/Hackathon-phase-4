# Task CRUD Operations Specification: Todo Backend

## Overview
This document specifies the Create, Read, Update, and Delete (CRUD) operations for tasks in the Todo application backend. These operations are secured with JWT authentication and enforce strict user isolation.

## Task Model Properties
- **id**: Integer, auto-generated unique identifier
- **title**: String, required (1-200 characters)
- **description**: String, optional (≤1000 characters)
- **completed**: Boolean, default false
- **due_date**: DateTime, optional
- **created_at**: DateTime, auto-generated on creation
- **updated_at**: DateTime, auto-generated on update
- **user_id**: UUID, foreign key referencing Better Auth user ID

## Operations

### Create Task
**Endpoint**: POST /api/{user_id}/tasks
**Authentication**: Required (JWT)
**Authorization**: User must match the user_id in the path

**Input Validation**:
- Title: Required, 1-200 characters
- Description: Optional, ≤1000 characters
- Due date: Optional, valid ISO datetime format
- User ID in path must match authenticated user

**Processing**:
1. Validate JWT token
2. Verify user_id in path matches authenticated user
3. Validate input data
4. Create new task record with provided data and authenticated user_id
5. Set created_at and updated_at to current timestamp
6. Return created task with 201 status

**Success Response**: 201 Created with created task object
**Error Responses**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 422 Validation Error

### Read All Tasks
**Endpoint**: GET /api/{user_id}/tasks
**Authentication**: Required (JWT)
**Authorization**: User must match the user_id in the path

**Query Parameters**:
- status: Optional, values: "all", "pending", "completed" (default: "all")
- sort: Optional, values: "created", "title", "due_date" (default: "created")

**Processing**:
1. Validate JWT token
2. Verify user_id in path matches authenticated user
3. Query tasks filtered by user_id
4. Apply status filter if specified
5. Apply sorting if specified
6. Return tasks array

**Success Response**: 200 OK with array of task objects
**Error Responses**: 401 Unauthorized, 403 Forbidden

### Read Single Task
**Endpoint**: GET /api/{user_id}/tasks/{id}
**Authentication**: Required (JWT)
**Authorization**: User must match the user_id in the path and own the task

**Processing**:
1. Validate JWT token
2. Verify user_id in path matches authenticated user
3. Query task by ID and user_id
4. Return task if found
5. Return 404 if not found

**Success Response**: 200 OK with task object
**Error Responses**: 401 Unauthorized, 403 Forbidden, 404 Not Found

### Update Task
**Endpoint**: PUT /api/{user_id}/tasks/{id}
**Authentication**: Required (JWT)
**Authorization**: User must match the user_id in the path and own the task

**Input Validation**:
- Title: Optional, if provided 1-200 characters
- Description: Optional, if provided ≤1000 characters
- Completed: Optional, boolean
- Due date: Optional, valid ISO datetime format

**Processing**:
1. Validate JWT token
2. Verify user_id in path matches authenticated user
3. Query task by ID and user_id to ensure ownership
4. Update provided fields
5. Update updated_at timestamp
6. Return updated task

**Success Response**: 200 OK with updated task object
**Error Responses**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Validation Error

### Toggle Task Completion
**Endpoint**: PATCH /api/{user_id}/tasks/{id}/complete
**Authentication**: Required (JWT)
**Authorization**: User must match the user_id in the path and own the task

**Input Validation**:
- Completed: Required, boolean value

**Processing**:
1. Validate JWT token
2. Verify user_id in path matches authenticated user
3. Query task by ID and user_id to ensure ownership
4. Update completion status
5. Update updated_at timestamp
6. Return updated task

**Success Response**: 200 OK with updated task object
**Error Responses**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Validation Error

### Delete Task
**Endpoint**: DELETE /api/{user_id}/tasks/{id}
**Authentication**: Required (JWT)
**Authorization**: User must match the user_id in the path and own the task

**Processing**:
1. Validate JWT token
2. Verify user_id in path matches authenticated user
3. Query task by ID and user_id to ensure ownership
4. Delete the task
5. Return 204 No Content

**Success Response**: 204 No Content
**Error Responses**: 401 Unauthorized, 403 Forbidden, 404 Not Found

## User Isolation
- Every query filters by the authenticated user's ID
- Users cannot access, modify, or delete tasks belonging to other users
- Path parameter user_id must match the authenticated user's ID
- Violations result in 403 Forbidden responses

## Validation Rules
- Title length: 1-200 characters
- Description length: ≤1000 characters
- Date formats: ISO 8601 format
- All inputs validated using Pydantic models
- Invalid data results in 422 Validation Error

## Error Handling
- Proper HTTP status codes for all scenarios
- Descriptive error messages without exposing sensitive information
- Consistent error response format
- Transactional operations to maintain data integrity

## Performance Considerations
- Efficient database queries with proper indexing
- Asynchronous operations for improved concurrency
- Pagination for large datasets (future enhancement)
- Caching for frequently accessed data (future enhancement)