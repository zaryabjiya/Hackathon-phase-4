# Quickstart Guide: Multi-User Todo Application

## Overview
This guide provides a quick start to set up and run the Multi-User Todo Application locally.

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Docker and Docker Compose (for database)
- Git

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/todo-fullstack-app.git
cd todo-fullstack-app
```

### 2. Set Up Environment Variables
Copy the example environment file and update the values:
```bash
cp .env.example .env
```

Required environment variables:
```env
# Backend
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
BETTER_AUTH_URL=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 3. Set Up the Backend
Navigate to the backend directory:
```bash
cd backend
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Set up the database using Docker:
```bash
docker-compose up -d
```

Run database migrations:
```bash
# This would typically be handled by the application startup
python -m src.main migrate
```

Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### 4. Set Up the Frontend
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

Install Node.js dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```

### 5. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

## Development Commands

### Backend
```bash
# Run tests
pytest

# Run with auto-reload
uvicorn src.main:app --reload

# Format code
black src tests

# Lint code
flake8 src tests
```

### Frontend
```bash
# Run tests
npm test

# Run linting
npm run lint

# Format code
npm run format

# Build for production
npm run build
```

## Project Structure
```
todo-fullstack-app/
├── backend/
│   ├── src/
│   │   ├── models/      # Database models
│   │   ├── api/         # API routes
│   │   ├── services/    # Business logic
│   │   ├── middleware/  # Authentication, etc.
│   │   └── utils/       # Utility functions
│   ├── tests/           # Backend tests
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/         # Next.js app router pages
│   │   ├── components/  # Reusable UI components
│   │   ├── lib/         # Utilities and API client
│   │   └── styles/      # Global styles
│   ├── tests/           # Frontend tests
│   ├── package.json     # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS config
├── docker-compose.yml   # Docker configuration
└── .env.example         # Environment variables example
```

## API Endpoints
For detailed API documentation, visit: http://localhost:8000/docs when the backend is running.

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Authenticate a user
- `POST /auth/logout` - Log out a user

### Tasks
- `GET /users/{user_id}/tasks` - Get user's tasks
- `POST /users/{user_id}/tasks` - Create a new task
- `GET /users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /users/{user_id}/tasks/{task_id}` - Update a task
- `PATCH /users/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /users/{user_id}/tasks/{task_id}` - Delete a task

## Troubleshooting

### Common Issues
1. **Database Connection Error**: Ensure Docker is running and the database service is up:
   ```bash
   docker-compose ps
   ```

2. **Port Already in Use**: Change the port in your `.env` file and application configuration.

3. **Dependency Issues**: Clear caches and reinstall:
   - Backend: `pip cache purge && pip install -r requirements.txt`
   - Frontend: `rm -rf node_modules && npm install`

### Resetting the Database
To reset the database to a clean state:
```bash
docker-compose down
docker-compose up -d
# Run migrations again
```

## Next Steps
1. Explore the API documentation at http://localhost:8000/docs
2. Review the frontend components in `frontend/src/components`
3. Add new features by following the established patterns
4. Write tests for any new functionality