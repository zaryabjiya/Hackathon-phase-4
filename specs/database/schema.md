# Database Schema Specification: Todo Backend

## Overview
This document specifies the database schema for the Todo application backend. The database uses Neon Serverless PostgreSQL with SQLModel for ORM operations. Better Auth manages user accounts, while our application manages tasks associated with users.

## Database Configuration
- **Database**: Neon Serverless PostgreSQL
- **Connection String**: Provided via `DATABASE_URL` environment variable
- **Driver**: asyncpg for asynchronous operations
- **ORM**: SQLModel (based on SQLAlchemy and Pydantic)

## Tables

### 1. tasks
Stores user tasks with strict ownership and isolation.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the task |
| title | VARCHAR(200) | NOT NULL | Task title (1-200 characters) |
| description | TEXT | NULL | Optional task description (≤1000 characters) |
| completed | BOOLEAN | DEFAULT FALSE | Task completion status |
| due_date | TIMESTAMP | NULL | Optional due date for the task |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp when the task was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() ON UPDATE | Timestamp when the task was last updated |
| user_id | UUID | NOT NULL, FOREIGN KEY | Reference to the user who owns this task |

**Indexes**:
- Primary Key: `id`
- Foreign Key: `user_id` (references users table managed by Better Auth)
- Composite Index: `(user_id, completed)` for efficient filtering by user and status
- Index: `due_date` for efficient sorting and filtering by due date

**Foreign Keys**:
- `user_id` references the `id` column in the users table managed by Better Auth

**Constraints**:
- `title` length must be between 1 and 200 characters
- `description` length must be ≤ 1000 characters
- `user_id` must reference an existing user in Better Auth's user table

## Better Auth Integration
The application relies on Better Auth to manage user accounts. The `user_id` in the `tasks` table references the user ID from Better Auth's user management system. The application does not directly manage user records but associates tasks with user IDs provided by the authentication system.

## Migration Strategy
- Use Alembic for database migrations
- Initialize schema with SQLModel's metadata.create_all() or equivalent migration
- Handle schema evolution with backward-compatible migrations
- Ensure zero-downtime deployments where possible

## Performance Considerations
- Indexes on user_id and status for efficient querying
- Proper indexing on due_date for sorting operations
- Connection pooling for optimal database performance
- Asynchronous operations to handle concurrent requests efficiently

## Security Considerations
- All data access is filtered by user_id to ensure user isolation
- No direct access to other users' data is possible
- Foreign key constraints ensure referential integrity
- Input validation prevents injection attacks