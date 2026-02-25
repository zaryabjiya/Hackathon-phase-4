# Next.js API Client Library Skill

## Description
This skill creates a comprehensive API client library for Next.js applications that handles HTTP requests to backend services, including authentication, error handling, and type safety.

## Purpose
- Create a centralized API client for Next.js frontend
- Handle authentication headers (JWT/Bearer tokens)
- Implement proper error handling and response parsing
- Provide typed request functions for all API endpoints
- Include request interceptors and response handling
- Output complete file with path: frontend/lib/api.ts
- Follow TypeScript best practices and Next.js conventions

## Implementation Requirements
- Use fetch API or axios for HTTP requests
- Include proper TypeScript interfaces/types for request/response payloads
- Handle authentication token inclusion in headers
- Implement error handling with proper error types
- Support common HTTP methods (GET, POST, PUT, DELETE)
- Include proper request/response type generics
- Handle loading states and error states appropriately
- Include proper imports (TypeScript types, etc.)
- Follow Next.js and React best practices

## Output Format
- Complete file content with API client implementation
- File path: frontend/lib/api.ts
- Include proper exports for different API endpoints
- Add JSDoc comments for all public functions
- Include example usage patterns

## Additional Considerations
- Include proper authentication token management
- Handle token refresh if needed
- Implement request cancellation if needed
- Add retry logic for failed requests if needed
- Include proper typing for all API endpoints
- Consider caching strategies
- Follow security best practices for token handling
- Include proper error messages for different HTTP status codes