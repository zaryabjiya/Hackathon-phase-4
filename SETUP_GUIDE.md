# TaskMaster - Complete Setup Guide

## 🚀 Quick Start (Windows)

### First Time Setup

1. **Run the setup script:**
```bash
.\start-dev.bat
```

This will:
- Set up the Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Start both backend and frontend servers

2. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Subsequent Runs

If dependencies are already installed, use:
```bash
.\start.bat
```

---

## 📋 Prerequisites

### Required Software

1. **Python 3.11 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 18 or higher**
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **PostgreSQL Database** (Choose one option):

   **Option A: Local PostgreSQL (Recommended for Development)**
   - Download from: https://www.postgresql.org/download/windows/
   - During installation:
     - Set postgres user password to `password`
     - Keep default port 5432

   **Option B: Neon Cloud Database (Free Tier)**
   - Go to: https://neon.tech
   - Create free account
   - Create new project
   - Copy connection string

---

## 🔧 Manual Setup (If Scripts Don't Work)

### Step 1: Database Setup

#### Local PostgreSQL:
```bash
# Run the provided script
.\setup-database.bat

# Or manually:
psql -U postgres
CREATE DATABASE todo_app;
ALTER USER postgres WITH PASSWORD 'password';
\q
```

#### Neon Cloud Database:
1. Create account at https://neon.tech
2. Create a new project
3. Copy the connection string from the dashboard

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Backend Configuration

Create `backend\.env` file:

**For Local PostgreSQL:**
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=true
```

**For Neon Database:**
```env
DATABASE_URL=postgresql+asyncpg://neondb_owner:YOUR_PASSWORD@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=true
```

### Step 4: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Step 5: Frontend Configuration

Create `frontend\.env.local` file:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Step 6: Start the Servers

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🧪 Testing the Setup

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy"}
```

### 2. Test User Registration

```bash
curl -X POST http://localhost:8000/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"username\":\"testuser\",\"password\":\"password123\"}"
```

Expected response:
```json
{
  "id": 1,
  "email": "test@example.com",
  "username": "testuser",
  "created_at": "2024-01-01T00:00:00",
  "is_active": true
}
```

### 3. Test User Login

```bash
curl -X POST http://localhost:8000/auth/login ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=test@example.com&password=password123"
```

Expected response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## ❌ Troubleshooting

### "Failed to fetch" Error

**Cause:** Frontend cannot connect to backend

**Solutions:**

1. **Check if backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```
   If this fails, start the backend:
   ```bash
   cd backend
   venv\Scripts\activate
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verify frontend environment:**
   Check `frontend\.env.local`:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

3. **Restart the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

### Database Connection Errors

**Error:** `could not connect to server`

**Solutions:**

1. **Check if PostgreSQL is running:**
   ```bash
   netstat -ano | findstr :5432
   ```

2. **Verify DATABASE_URL in `backend\.env`:**
   - Local: `postgresql+asyncpg://postgres:password@localhost:5432/todo_app`
   - Neon: Include `?sslmode=require`

3. **Test database connection:**
   ```bash
   psql -U postgres -h localhost -d todo_app
   ```

4. **For Neon database:**
   - Check IP whitelist settings
   - Verify connection string format
   - Ensure `?sslmode=require` is included

### CORS Errors

**Error:** `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution:**

The backend already allows these origins:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3001`

If using a different port, update `backend\main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "YOUR_PORT"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Backend Won't Start

**Check Python version:**
```bash
python --version
```
Should be 3.11 or higher.

**Reinstall dependencies:**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

**Check for port conflicts:**
```bash
netstat -ano | findstr :8000
```

If port 8000 is in use, either:
1. Kill the process using port 8000
2. Or change the port in `backend\main.py`:
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```
   Then update `frontend\.env.local`:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
   ```

### Frontend Build Errors

**Clear Next.js cache:**
```bash
cd frontend
rm -rf .next
npm run dev
```

**Reinstall node modules:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### "ModuleNotFoundError: No module named 'X'"

**Solution:**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### JWT/Authentication Errors

**Error:** `Could not validate credentials`

**Solutions:**

1. **Verify SECRET_KEY is set in `backend\.env`:**
   ```env
   SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-make-it-long-and-random
   ```

2. **Clear browser localStorage:**
   - Open DevTools (F12)
   - Go to Application tab
   - Clear localStorage
   - Try logging in again

3. **Check token format in requests:**
   - Should be: `Authorization: Bearer YOUR_TOKEN`

---

## 📚 API Documentation

Once backend is running, access:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Available Endpoints

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login user |
| POST | `/auth/logout` | Logout user |

#### Tasks (require authentication)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/{user_id}/tasks` | Get all tasks |
| POST | `/users/{user_id}/tasks` | Create task |
| GET | `/users/{user_id}/tasks/{task_id}` | Get specific task |
| PUT | `/users/{user_id}/tasks/{task_id}` | Update task |
| PATCH | `/users/{user_id}/tasks/{task_id}/complete` | Toggle completion |
| DELETE | `/users/{user_id}/tasks/{task_id}` | Delete task |

---

## 🎯 Usage Guide

### 1. Register a New Account

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Fill in:
   - Username
   - Email
   - Password
4. Click "Sign up"

### 2. Login

1. Go to http://localhost:3000/auth/login
2. Enter email and password
3. Click "Sign in"

### 3. Manage Tasks

**Create Task:**
1. Click "Add Task" button
2. Fill in title (required)
3. Add description (optional)
4. Set due date (optional)
5. Click "Create Task"

**Update Task:**
1. Click on a task to view details
2. Edit fields as needed
3. Click "Save Changes"

**Complete Task:**
- Click the checkbox next to any task

**Delete Task:**
1. Click on a task
2. Click "Delete Task"
3. Confirm deletion

---

## 📁 Project Structure

```
todo-phs-ii/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── tasks.py         # Task endpoints
│   ├── models/
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   ├── db/
│   │   └── session.py       # Database connection
│   ├── .env                 # Backend environment (create from .env.example)
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js pages
│   │   ├── components/      # React components
│   │   ├── providers/       # Context providers
│   │   └── lib/             # Utilities
│   ├── .env.local           # Frontend environment
│   └── package.json         # Node.js dependencies
├── start.bat                # Quick start script
├── start-dev.bat            # Full setup script
└── README.md                # This file
```

---

## 🔐 Security Notes

- Never commit `.env` files to version control
- Change `SECRET_KEY` in production
- Use strong passwords
- Enable HTTPS in production
- Implement rate limiting for production

---

## 🆘 Still Having Issues?

1. **Check the logs:**
   - Backend logs in the backend terminal window
   - Frontend logs in the frontend terminal window
   - Browser console (F12) for frontend errors

2. **Verify all prerequisites are installed:**
   ```bash
   python --version
   node --version
   npm --version
   ```

3. **Try a clean restart:**
   ```bash
   # Stop all servers (close terminal windows)

   # Restart backend
   cd backend
   venv\Scripts\activate
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # In new terminal, restart frontend
   cd frontend
   npm run dev
   ```

4. **Check database connectivity:**
   - For local: `psql -U postgres -h localhost -d todo_app`
   - For Neon: Check IP whitelist and connection string

---

## 🎉 Success Indicators

You know everything is working when:

1. ✅ Backend responds to `http://localhost:8000/health`
2. ✅ Frontend loads at `http://localhost:3000`
3. ✅ You can register a new user
4. ✅ You can login with your credentials
5. ✅ You can create, update, and delete tasks
6. ✅ No console errors in browser (F12)

---

**Happy Task Managing! 🚀**
