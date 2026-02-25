# Data Model: Multi-User Todo Application

## Overview
This document defines the data model for the multi-user Todo application, including entities, relationships, and validation rules.

## Entities

### User
**Description**: Represents an application user with authentication credentials

**Fields**:
- `id` (UUID/string): Unique identifier for the user
- `email` (string): User's email address (unique, required)
- `hashed_password` (string): BCrypt hashed password (required)
- `first_name` (string, optional): User's first name
- `last_name` (string, optional): User's last name
- `is_active` (boolean): Whether the account is active (default: true)
- `created_at` (datetime): Timestamp when the user was created
- `updated_at` (datetime): Timestamp when the user was last updated

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements
- First name and last name must be 1-50 characters if provided

**State Transitions**:
- Active → Inactive (account deactivation)
- Inactive → Active (account reactivation)

### Task
**Description**: Represents a todo item owned by a user

**Fields**:
- `id` (UUID/string): Unique identifier for the task
- `title` (string): Task title (required, 1-200 characters)
- `description` (string, optional): Task description (≤1000 characters)
- `completed` (boolean): Whether the task is completed (default: false)
- `completed_at` (datetime, optional): Timestamp when the task was completed
- `due_date` (datetime, optional): Deadline for the task
- `priority` (enum): Priority level (low, medium, high) (default: medium)
- `user_id` (UUID/string): Foreign key linking to the owning user
- `created_at` (datetime): Timestamp when the task was created
- `updated_at` (datetime): Timestamp when the task was last updated

**Validation Rules**:
- Title must be 1-200 characters
- Description must be ≤1000 characters if provided
- Due date must be in the future if provided
- Priority must be one of the allowed values
- User ID must reference an existing user

**State Transitions**:
- Pending → Completed (when task is marked as done)
- Completed → Pending (when task is marked as undone)

## Relationships

### User → Task (One-to-Many)
- A user can own many tasks
- Each task belongs to exactly one user
- Foreign key: `user_id` in the Task entity references `id` in the User entity
- Cascade delete: When a user is deleted, all their tasks are also deleted

## Indexes

### User Entity
- Primary index on `id`
- Unique index on `email`
- Index on `created_at` for chronological queries

### Task Entity
- Primary index on `id`
- Index on `user_id` for efficient user-specific queries
- Index on `completed` for filtering completed/pending tasks
- Index on `due_date` for deadline-based queries
- Index on `created_at` for chronological ordering
- Composite index on (`user_id`, `completed`) for common user-task queries

## Constraints

### Data Integrity
- Referential integrity: All foreign key relationships must reference existing records
- Unique constraints: Email addresses must be unique across users
- Check constraints: 
  - Task title length (1-200 characters)
  - Task description length (≤1000 characters)
  - Due date must be in the future if provided

### Business Logic
- Users can only access their own tasks
- Completed tasks retain their completion timestamp
- Updating a completed task clears the completion timestamp