# Backend Implementation Plan: Todo Full-Stack Web Application (Phase II)

## 1. High-Level Overview

### Summary of Backend Deliverables
- Complete FastAPI backend with JWT authentication
- Neon Serverless PostgreSQL integration with SQLModel
- Better Auth server-side integration for user management
- Secure task CRUD operations with strict user isolation
- Production-ready API with proper error handling and validation

### Key Milestones
1. Project setup and database connection
2. Authentication integration with Better Auth
3. JWT middleware implementation
4. Task models and database schema
5. Task CRUD routes with user isolation
6. Security and validation layers
7. Testing and validation
8. Final integration and deployment preparation

## 2. Phased Implementation Steps

### Phase 1: Project Setup and Dependencies
**Goal**: Establish project structure and install required dependencies
**Dependencies**: None
**Files to create/modify**: 
- backend/requirements.txt
- backend/.env
- backend/.gitignore
- backend/main.py (initial)

**Key features/techniques**:
- Install FastAPI, SQLModel, uvicorn, better-auth, pyjwt, pydantic, python-dotenv
- Set up .env with required variables
- Create basic FastAPI app structure

**Delegate to**: backend-agent
**Estimated complexity**: Low
**Acceptance criteria**: 
- Project structure created
- Dependencies installed successfully
- Basic FastAPI app runs without errors

### Phase 2: Database Setup and Connection
**Goal**: Configure Neon PostgreSQL connection with SQLModel
**Dependencies**: Phase 1
**Files to create/modify**: 
- backend/db.py
- backend/models.py (initial)
- backend/main.py (update with DB connection)

**Key features/techniques**:
- SQLModel async engine with DATABASE_URL
- Proper SSL configuration for Neon
- Database session dependency

**Delegate to**: backend-agent
**Estimated complexity**: Medium
**Acceptance criteria**: 
- Successful connection to Neon DB
- Database session dependency working
- No connection errors on startup

### Phase 3: Better Auth Server Integration
**Goal**: Set up Better Auth server-side with JWT plugin
**Dependencies**: Phase 1
**Files to create/modify**: 
- backend/auth.py
- backend/main.py (mount auth routes)

**Key features/techniques**:
- Better Auth server instance with JWT plugin
- Mount auth routes at /api/auth/*
- Use BETTER_AUTH_SECRET for JWT signing

**Delegate to**: backend-agent
**Estimated complexity**: Medium
**Acceptance criteria**: 
- Auth routes accessible at /api/auth/*
- JWT tokens generated on login
- Proper secret configuration

### Phase 4: Task Model and Schema
**Goal**: Create Task model with proper relationships and constraints
**Dependencies**: Phase 2
**Files to create/modify**: 
- backend/models.py (complete)
- backend/db.py (update with model creation)

**Key features/techniques**:
- SQLModel Task model with all required fields
- Proper indexing for performance
- Relationship to Better Auth user ID
- Validation constraints (title length, description length)

**Delegate to**: sqlmodel-task-model
**Estimated complexity**: Medium
**Acceptance criteria**: 
- Task model created with all required fields
- Proper database schema generated
- Validation constraints implemented

### Phase 5: JWT Verification Middleware
**Goal**: Implement JWT middleware for protected routes
**Dependencies**: Phase 3
**Files to create/modify**: 
- backend/middleware/auth.py
- backend/main.py (add middleware)

**Key features/techniques**:
- JWT token extraction from Authorization header
- Verification with BETTER_AUTH_SECRET
- User ID extraction and validation
- Path user_id matching with token user_id

**Delegate to**: jwt-fastapi-middleware
**Estimated complexity**: High
**Acceptance criteria**: 
- Valid tokens allow access to protected routes
- Invalid tokens return 401 Unauthorized
- Mismatched user_ids return 403 Forbidden

### Phase 6: Task CRUD Routes Implementation
**Goal**: Implement all required task CRUD operations
**Dependencies**: Phases 4, 5
**Files to create/modify**: 
- backend/routes/tasks.py
- backend/main.py (include router)

**Key features/techniques**:
- All required endpoints implemented
- User isolation enforced in every query
- Proper input validation with Pydantic
- Correct HTTP status codes

**Delegate to**: tasks-crud-routes-fastapi
**Estimated complexity**: High
**Acceptance criteria**: 
- All endpoints return correct data
- User isolation working properly
- Input validation functioning
- Correct HTTP status codes returned

### Phase 7: Error Handling and Validation
**Goal**: Implement comprehensive error handling and validation
**Dependencies**: Phase 6
**Files to create/modify**: 
- backend/exceptions.py
- backend/routes/tasks.py (update with error handling)

**Key features/techniques**:
- Custom HTTP exceptions
- Proper error responses
- Validation error handling
- Logging for debugging

**Delegate to**: error-handling-global
**Estimated complexity**: Medium
**Acceptance criteria**: 
- Proper error responses for all scenarios
- Validation errors handled correctly
- Logging implemented for debugging

### Phase 8: Security and Performance Enhancements
**Goal**: Add security headers, CORS, and performance optimizations
**Dependencies**: All previous phases
**Files to create/modify**: 
- backend/main.py (CORS, security headers)
- backend/middleware/security.py (optional)

**Key features/techniques**:
- CORS configuration for frontend (http://localhost:3000)
- Security headers
- Request/response validation
- Performance optimizations

**Delegate to**: backend-agent
**Estimated complexity**: Medium
**Acceptance criteria**: 
- CORS configured for frontend origin
- Security headers added
- Performance optimizations in place

### Phase 9: Testing and Validation
**Goal**: Create comprehensive tests and validate functionality
**Dependencies**: All previous phases
**Files to create/modify**: 
- backend/tests/test_tasks.py
- backend/tests/conftest.py
- backend/pytest.ini (if needed)

**Key features/techniques**:
- Unit tests for all endpoints
- Authentication tests
- Error condition tests
- Integration tests

**Delegate to**: test-crud-endpoints
**Estimated complexity**: High
**Acceptance criteria**: 
- All tests passing
- Authentication flows tested
- Error conditions covered
- Integration tests validate complete flow

### Phase 10: Final Integration and Deployment Preparation
**Goal**: Prepare for final integration with frontend
**Dependencies**: All previous phases
**Files to create/modify**: 
- backend/Dockerfile (optional)
- backend/docker-compose.yml (optional)
- backend/README.md
- backend/pyproject.toml (if using poetry)

**Key features/techniques**:
- Documentation updates
- Deployment configuration
- Environment validation
- Final security checks

**Delegate to**: backend-agent
**Estimated complexity**: Low
**Acceptance criteria**: 
- Documentation complete
- Deployment configuration ready
- Final security validation passed

## 3. Delegation Table

| Phase # | Task Description                          | Delegate To (agent/skill)      | Priority | Files Involved                  |
|---------|------------------------------------------|-------------------------------|----------|---------------------------------|
| 1       | Project setup and dependencies           | backend-agent                 | High     | requirements.txt, .env, main.py |
| 2       | Database setup and connection            | backend-agent                 | High     | db.py, models.py, main.py       |
| 3       | Better Auth server integration           | backend-agent                 | High     | auth.py, main.py                |
| 4       | Task model and schema                    | sqlmodel-task-model           | High     | models.py, db.py                |
| 5       | JWT verification middleware              | jwt-fastapi-middleware        | Critical | middleware/auth.py, main.py     |
| 6       | Task CRUD routes implementation          | tasks-crud-routes-fastapi     | Critical | routes/tasks.py, main.py        |
| 7       | Error handling and validation            | error-handling-global         | High     | exceptions.py, routes/tasks.py  |
| 8       | Security and performance enhancements    | backend-agent                 | Medium   | main.py, middleware/security.py |
| 9       | Testing and validation                   | test-crud-endpoints           | High     | tests/test_tasks.py             |
| 10      | Final integration and deployment prep    | backend-agent                 | Medium   | README.md, Dockerfile, etc.     |

## 4. Prerequisites & Setup Reminders

### Required Packages to Install
```bash
pip install fastapi==0.115.0
pip install sqlmodel==0.0.22
pip install uvicorn[standard]==0.32.0
pip install better-auth==0.2.1
pip install pyjwt==2.10.1
pip install pydantic==2.10.3
pip install python-dotenv==1.0.1
pip install psycopg2-binary==2.10.1
pip install alembic==1.14.0  # if migrations needed
```

### Environment Loading
```python
# In main.py
from dotenv import load_dotenv
load_dotenv()
```

### Neon DB Connection
```python
# Use SQLModel.create_engine with DATABASE_URL
# Ensure SSL parameters are handled correctly
```

## 5. Security & Integration Phase

### JWT Verification Middleware
- Verify signature with BETTER_AUTH_SECRET
- Extract user_id from token payload
- Attach user info to request.state.user
- Validate path {user_id} matches token user_id

### User Isolation Enforcement
- In every DB query: `.where(Task.user_id == current_user.id)`
- Prevent access to other users' data
- Return 403 Forbidden for unauthorized access

### Better Auth Server Integration
- Mount auth routes at /api/auth/*
- Enable JWT plugin on server side
- Configure with shared secret

## 6. Testing & Validation Phase

### Manual Testing Checklist
- [ ] curl/postman for each endpoint with/without token
- [ ] Test wrong user_id scenarios
- [ ] Validate input validation (title 1-200, desc ≤1000)
- [ ] Test all error conditions (401, 403, 404, 422)
- [ ] Verify timestamps are correctly set

### Pytest Suggestions
- test_tasks.py for CRUD operations
- Authentication failure tests
- User isolation tests
- Input validation tests

### Integration Check
- Run backend + frontend together
- Test sign-in → tasks fetch
- Verify JWT token flow works end-to-end

## 7. Output Format

### File Structure
```
backend/
├── main.py
├── .env
├── .gitignore
├── requirements.txt
├── db.py
├── models.py
├── auth.py
├── middleware/
│   └── auth.py
├── routes/
│   └── tasks.py
├── exceptions.py
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
└── README.md
```

### Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
cd backend && uvicorn main:app --reload --port 8000

# Run tests
cd backend && pytest
```

After this plan is approved, start delegation with phase 1 using main-agent or backend-agent. Then run: `cd backend && uvicorn main:app --reload --port 8000`