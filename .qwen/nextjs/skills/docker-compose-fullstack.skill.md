# Docker Compose Fullstack Skill

## Description
This skill creates a professional docker-compose.yml file for deploying the complete Todo application stack including Next.js frontend, FastAPI backend, and PostgreSQL database (either Neon proxy or local PostgreSQL).

## Purpose
- Create a docker-compose.yml file for the fullstack application
- Configure services for Next.js frontend, FastAPI backend, and PostgreSQL
- Support both Neon proxy and local PostgreSQL configurations
- Include proper networking, volumes, and environment configuration
- Output complete docker-compose.yml file with professional setup
- Ensure services can communicate properly within the compose network

## Implementation Requirements
- Define service for Next.js frontend with proper build context
- Define service for FastAPI backend with proper dependencies
- Configure PostgreSQL service (local) or Neon proxy connection
- Set up proper environment variables for all services
- Configure volumes for persistent data and shared resources
- Define proper ports mapping for external access
- Set up health checks for services
- Configure restart policies
- Include proper service dependencies and startup order
- Add nginx reverse proxy if needed for production setup

## Output Format
- Complete docker-compose.yml file content
- File path: docker-compose.yml
- Include all necessary services and configurations
- Add comments explaining key configuration choices
- Include environment variable examples
- Add documentation for deployment options
- Provide full YAML content with all configurations
- Include detailed usage instructions for deployment

## Additional Considerations
- Implement proper security measures in container configuration
- Consider resource limits and scaling options
- Include backup and restore procedures if needed
- Add monitoring and logging configurations
- Consider multi-stage builds for optimized images
- Implement secrets management for sensitive data
- Include configuration for different environments (dev, staging, prod)
- Add proper health check endpoints
- Consider using .env files for environment-specific configurations