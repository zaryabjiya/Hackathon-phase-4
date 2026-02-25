# Error Handling Skill

## Description
This skill implements comprehensive error handling for both frontend (Next.js) and backend (FastAPI) components of the Todo application. It ensures consistent error responses, proper error boundaries, and user-friendly error messages.

## Purpose
- Implement backend error handling with proper HTTP status codes
- Create frontend error boundaries and error display components
- Establish consistent error response formats
- Handle validation errors appropriately on both sides
- Implement proper logging for debugging
- Output complete code for both frontend and backend error handling
- Follow best practices for error handling in both frameworks

## Implementation Requirements
- Create custom exception handlers for FastAPI backend
- Define consistent error response models for API endpoints
- Implement validation error handling with proper status codes
- Create error boundary components for Next.js frontend
- Implement error display components with user-friendly messages
- Add logging configuration for error tracking
- Handle network errors and offline states in frontend
- Create error utility functions for both sides
- Include proper TypeScript types for error objects in frontend
- Follow security best practices (don't expose sensitive info in errors)

## Output Format
- Complete backend error handling code
- File path: backend/app/utils/exceptions.py
- Complete frontend error handling code
- File path: frontend/src/components/ErrorBoundary.tsx
- Additional error utility files as needed
- Include proper imports and module structure
- Add documentation for error handling patterns
- Output code for both frontend and backend as requested

## Additional Considerations
- Implement centralized error reporting if needed
- Consider using error reporting services (Sentry, etc.)
- Ensure error messages are translatable if needed
- Add appropriate error monitoring and alerting
- Handle different error types appropriately
- Implement graceful degradation for critical errors
- Follow accessibility guidelines for error messages
- Include proper error tracking for analytics