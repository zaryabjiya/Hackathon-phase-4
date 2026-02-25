# Authentication Middleware Skill

## Description
This skill implements authentication middleware for FastAPI applications that handles JWT token validation, user payload attachment, and protected route dependencies. It follows security best practices for token validation and error handling.

## Purpose
- Read secret from environment variable (os.getenv("BETTER_AUTH_SECRET"))
- Validate JWT signature, expiry, and audience claims
- Attach authenticated user payload to request.state.user
- Raise appropriate HTTP exceptions (401 for invalid token, 403 for insufficient permissions)
- Provide dependency for protecting routes
- Output complete implementation with proper file structure

## Implementation Requirements
- Use os.getenv to read BETTER_AUTH_SECRET from environment
- Validate JWT signature using the secret
- Check token expiration (exp claim)
- Verify audience (aud claim) if specified
- Attach user payload to request.state.user for downstream handlers
- Raise HTTPException with status 401 for invalid/missing tokens
- Raise HTTPException with status 403 for insufficient permissions
- Create a dependency function for use with FastAPI route protection
- Include proper type hints and error handling
- Follow FastAPI security best practices

## Output Format
- Complete code block with proper imports and implementation
- File path: backend/middleware/auth.py
- Include comprehensive error handling
- Add documentation for the middleware and dependency functions

## Security Considerations
- Never expose secrets in code
- Validate all token claims properly
- Use secure comparison for token validation
- Implement proper error responses that don't leak information
- Follow OWASP security recommendations for JWT handling

## Dependencies
- fastapi
- python-jose[cryptography] or similar JWT library
- pydantic
- typing
- os