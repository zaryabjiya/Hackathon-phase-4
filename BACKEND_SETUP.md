# Backend Quick Start Guide

## Problem: "Failed to fetch" Error

The error occurs because the frontend cannot connect to the backend API. This happens when:
1. The backend server is not running
2. The database is not accessible
3. CORS is misconfigured

## Solution

### Option 1: Using Local PostgreSQL (Recommended for Development)

#### Step 1: Install PostgreSQL

Download and install PostgreSQL from: https://www.postgresql.org/download/windows/

During installation:
- Set the password for the `postgres` user to `password` (or update `.env` accordingly)
- Keep the default port 5432

#### Step 2: Create the Database

Run the setup script:
```bash
.\setup-database.bat
```

Or manually:
```bash
psql -U postgres
CREATE DATABASE todo_app;
ALTER USER postgres WITH PASSWORD 'password';
\q
```

#### Step 3: Verify Backend Configuration

Ensure `backend\.env` contains:
```
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Step 4: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Step 5: Start the Backend

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Step 6: Test the Backend

Open a new terminal and test:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy"}
```

#### Step 7: Start the Frontend

In another terminal:
```bash
cd frontend
npm run dev
```

### Option 2: Using a Cloud Database (Neon)

#### Step 1: Create a Neon Database

1. Go to https://neon.tech
2. Create a free account
3. Create a new project
4. Copy the connection string

#### Step 2: Update Backend Configuration

Edit `backend\.env`:
```
DATABASE_URL=postgresql+asyncpg://<your-neon-connection-string>
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Step 3: Start the Backend

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the backend is running, access the interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout

### Tasks
- `GET /users/{user_id}/tasks` - Get all tasks for a user
- `POST /users/{user_id}/tasks` - Create a new task
- `GET /users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /users/{user_id}/tasks/{task_id}` - Update a task
- `PATCH /users/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /users/{user_id}/tasks/{task_id}` - Delete a task

## Troubleshooting

### Backend won't start

1. Check if Python 3.11+ is installed:
   ```bash
   python --version
   ```

2. Verify dependencies are installed:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Check database connection:
   ```bash
   psql -U postgres -h localhost -d todo_app
   ```

### CORS Errors

The backend is configured to allow requests from `http://localhost:3000`. If you're using a different port, update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Connection Errors

1. Verify PostgreSQL is running:
   ```bash
   netstat -ano | findstr :5432
   ```

2. Check the DATABASE_URL format in `backend\.env`

3. For Neon/Cloud databases, ensure your IP is whitelisted

## Testing with curl

### Register a user:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"username\":\"testuser\",\"password\":\"password123\"}"
```

### Login:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

### Get tasks (replace TOKEN and USER_ID):
```bash
curl http://localhost:8000/users/1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
