# Better Auth Implementation Skill

## Description
This skill implements Better Auth for both frontend and backend authentication in the Todo application. It handles user registration, login, logout, and protected routes with JWT tokens.

## Purpose
- Set up Better Auth for the Next.js/FastAPI application
- Configure authentication providers and user management
- Implement protected routes on both frontend and backend
- Handle JWT token management and validation
- Output complete code blocks for auth configuration
- Include installation note: npm i better-auth
- Ensure secure authentication practices

## Implementation Requirements
- Configure Better Auth with proper secret and database settings
- Implement user registration and login endpoints
- Set up session management and JWT handling
- Create middleware for protecting routes
- Handle authentication state on the frontend
- Implement proper error handling for auth operations
- Include proper TypeScript types for auth objects
- Follow security best practices for credential handling
- Ensure proper integration with the existing database

## Output Format
- Complete code blocks for auth configuration files
- Backend auth API routes (backend/app/auth/)
- Frontend auth integration (frontend/src/lib/auth.ts)
- Configuration files for both frontend and backend
- Installation note: npm i better-auth
- Include proper imports and module structure
- Add documentation for auth functions and components

## Additional Considerations
- Implement proper password validation and hashing
- Add account verification/email confirmation if needed
- Include password reset functionality
- Handle concurrent session management
- Implement proper logout functionality
- Add CSRF protection where appropriate
- Consider rate limiting for auth endpoints
- Ensure secure storage of sensitive data
- Follow OAuth best practices if external providers are used