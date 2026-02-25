# SQLModel Task Model Skill

## Description
This skill creates a SQLModel model for a Task entity with proper relationships, validation, and database configuration. It generates the complete model definition and suggests migration notes for database updates.

## Purpose
- Create a Task model using SQLModel (SQLAlchemy + Pydantic)
- Include appropriate fields for a todo application (title, description, status, etc.)
- Define proper relationships with User model for multi-user support
- Add validation and constraints as needed
- Output complete code block with file path: backend/models.py
- Include suggested migration notes for database updates

## Implementation Requirements
- Use SQLModel base class with table=True for database models
- Include common fields: id, title, description, status, created_at, updated_at
- Add foreign key relationship to User model for user ownership
- Include proper indexing for frequently queried fields
- Add validation for required fields
- Use appropriate data types (str, int, datetime, bool, etc.)
- Include proper imports (SQLModel, Field, Relationship, etc.)
- Follow database normalization principles

## Output Format
- Complete code block with Task model definition
- File path: backend/models.py
- Include suggested migration notes for Alembic
- Show how the model relates to other entities (User, etc.)

## Additional Considerations
- Include proper nullable and default value specifications
- Add constraints where appropriate (e.g., max length for text fields)
- Consider soft deletion if needed (deleted_at field)
- Include proper indexing for performance
- Follow naming conventions for database columns
- Consider adding custom methods if needed for business logic