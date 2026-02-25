# Authentication Specification: Todo Backend

## Overview
This document specifies the authentication system for the Todo application backend. The system leverages Better Auth for comprehensive user management and JWT-based authentication. The backend verifies JWT tokens on protected endpoints to ensure secure access to user data.

## Authentication System
- **Provider**: Better Auth (server-side)
- **Token Type**: JWT (JSON Web Tokens)
- **Signing Algorithm**: HS256 with shared secret
- **Token Expiration**: 7 days (configurable in Better Auth)
- **Secret Management**: Stored in environment variable `BETTER_AUTH_SECRET`

## Environment Variables
- `BETTER_AUTH_SECRET`: Shared secret for JWT signing/verification (aPwV1FM8W5bmHF7o7xCgsq5PDACVaNFO)
- `DATABASE_URL`: Neon Serverless PostgreSQL connection string

## JWT Token Structure
The JWT tokens issued by Better Auth contain the following claims:
- `sub`: Subject (user ID)
- `exp`: Expiration time
- `iat`: Issued at time
- `jti`: JWT ID (for potential revocation)
- Additional user claims as configured in Better Auth

## Token Verification Process
1. Extract JWT token from `Authorization: Bearer <token>` header
2. Verify token signature using `BETTER_AUTH_SECRET`
3. Check token expiration
4. Decode user information (user ID, email)
5. Validate that the user ID in the token matches the user ID in the request path
6. Return user information for use in request processing

## Protected Endpoints
All task-related endpoints require JWT authentication:
- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- GET /api/{user_id}/tasks/{id}
- PUT /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH /api/{user_id}/tasks/{id}/complete

## Authentication Middleware
The backend implements a FastAPI dependency for JWT verification:
- `get_current_user()` dependency that validates JWT and extracts user info
- Returns user ID and email for use in request handlers
- Raises 401 Unauthorized for invalid/missing tokens
- Raises 403 Forbidden when path user_id doesn't match token user_id

## Error Handling
- 401 Unauthorized: Invalid, expired, or missing JWT token
- 403 Forbidden: User attempting to access resources they don't own
- Proper error messages without exposing sensitive information

## Integration with Better Auth
- Better Auth handles user registration, login, and session management
- Better Auth issues JWT tokens upon successful authentication
- Our backend verifies these tokens without managing user credentials
- User data is managed by Better Auth; our backend only stores task associations

## Security Measures
- Strong secret key for JWT signing
- Short token lifetime (7 days) to minimize exposure risk
- Strict user isolation - users can only access their own data
- Input validation to prevent injection attacks
- Secure transport (HTTPS in production) required for all authentication flows

## Token Refresh
- Better Auth handles token refresh automatically
- Frontend is responsible for refreshing tokens before expiration
- Backend does not implement token refresh endpoints