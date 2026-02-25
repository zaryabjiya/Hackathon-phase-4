# Backend Integration Specification: Todo Application

## Overview
This document specifies the integration points between the various components of the Todo application backend. It covers the JWT authentication middleware, database setup, and how the different parts work together to provide a secure and efficient API.

## Architecture Components

### FastAPI Application
- **Framework**: FastAPI for high-performance ASGI web framework
- **Mounting**: Better Auth endpoints mounted at `/api/auth/*`
- **Custom Routes**: Task endpoints under `/api/*` namespace
- **Middleware**: JWT verification middleware for protected routes
- **Dependency Injection**: FastAPI's dependency system for authentication and database access

### Database Layer
- **ORM**: SQLModel (combines SQLAlchemy and Pydantic)
- **Engine**: Async engine for PostgreSQL connection
- **Connection**: Using DATABASE_URL environment variable
- **Session Management**: Dependency injection for database sessions
- **Models**: Defined with SQLModel for type safety and validation

### Authentication Layer
- **Provider**: Better Auth server-side instance
- **Token Verification**: Custom JWT middleware using PyJWT
- **User Validation**: Ensures path user_id matches token user_id
- **Dependency**: `get_current_user()` for route protection

## Database Setup

### Engine Configuration
```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

### Model Registration
- SQLModel metadata registered with all models
- Automatic table creation using `SQLModel.metadata.create_all(engine)`
- Proper relationship definitions between entities
- Index definitions for performance optimization

### Session Dependency
```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

## JWT Middleware Implementation

### Token Extraction
- Extract token from `Authorization: Bearer <token>` header
- Validate presence and format of token
- Handle missing or malformed authorization headers

### Token Verification
- Decode JWT using `BETTER_AUTH_SECRET`
- Verify token signature and expiration
- Extract user information (user_id, email)
- Validate that path user_id matches token user_id

### Current User Dependency
```python
def get_current_user(authorization: str = Header(...)) -> dict:
    # Extract and verify JWT
    # Validate user_id match
    # Return user information
```

## Better Auth Integration

### Server-Side Instance
```python
from better_auth import auth
from better_auth.plugins.jwt import jwt

auth_instance = auth(
    secret=os.getenv("BETTER_AUTH_SECRET"),
    plugins=[jwt()]
)
```

### Mounting in FastAPI
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.mount("/api/auth", auth_instance.app)
```

### Token Generation
- Better Auth generates JWT tokens upon successful authentication
- Tokens contain user information and expiration
- Tokens signed with shared secret for verification

## Error Handling Strategy

### HTTP Exception Handling
- Custom exception handlers for different error types
- Consistent error response format
- Proper HTTP status codes
- Logging for debugging and monitoring

### Validation Errors
- Pydantic models for request/response validation
- 422 responses for validation failures
- Detailed error messages for debugging

## Security Measures

### Input Validation
- Pydantic models for all request/response bodies
- Type checking and validation at the API boundary
- Sanitization of user inputs

### Access Control
- JWT-based authentication for all protected routes
- User ID verification in path parameters
- Strict user isolation for data access

### Secret Management
- Environment variables for sensitive configuration
- No hardcoded secrets in source code
- Secure handling of JWT secrets

## Performance Considerations

### Asynchronous Operations
- Async database operations using asyncpg
- Non-blocking I/O for improved concurrency
- Proper async/await patterns throughout

### Connection Pooling
- Configured connection pool for database
- Optimized pool size for expected load
- Proper connection lifecycle management

### Caching (Future Enhancement)
- Potential caching layer for frequently accessed data
- Cache invalidation strategies
- Redis or similar for distributed caching

## Logging and Monitoring

### Request Logging
- Log incoming requests with relevant information
- Response status codes and processing time
- Error logging with stack traces

### Security Logging
- Authentication attempts and failures
- Authorization violations
- Suspicious access patterns

## Deployment Considerations

### Environment Configuration
- Docker-ready configuration
- Environment variable-based configuration
- Separate configurations for development, staging, and production

### Health Checks
- Health check endpoints for container orchestration
- Database connectivity checks
- External service dependency checks

### Scaling
- Stateless design for horizontal scaling
- Database connection management for multiple instances
- Load balancing considerations

## Testing Strategy

### Unit Tests
- Individual function and method testing
- Mocking of external dependencies
- Coverage of edge cases and error conditions

### Integration Tests
- End-to-end API testing
- Database integration testing
- Authentication flow testing

### Security Testing
- Authentication bypass attempts
- Authorization validation
- Input validation testing