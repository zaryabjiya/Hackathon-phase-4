---
id: 1
title: "Create Todo App Constitution"
stage: constitution
date_iso: "2026-02-13"
surface: "agent"
model: "Claude Sonnet 4"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution Create or update the project's constitution.md file with governing principles"
labels: ["constitution", "governance", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
  - "history/prompts/constitution/1-create-todo-app-constitution.constitution.prompt.md"
tests_yaml: []
outcome: "Successfully created the project constitution for the Todo Full-Stack Web Application with comprehensive principles covering spec-first development, agent-based implementation, security requirements, technology stack adherence, API contract compliance, and quality standards."
evaluation: "The constitution document was successfully created with all required sections and principles. It establishes clear governance for the project and will guide all future development activities."
---

# Create Todo App Constitution

## User Input

Create or update the project's constitution.md file with governing principles, development guidelines, and rules that will guide ALL future AI-assisted development in this monorepo.

Project context: This is Phase II of a Todo Full-Stack Web Application hackathon project. Transforming a console app into a modern multi-user web app with persistent storage.

Core stack and rules:
- Monorepo structure: .spec-kit/config.yaml, specs/ (organized by overview.md, features/, api/, database/, ui/), CLAUDE.md (root + frontend/ + backend/), frontend/ (Next.js 16+ App Router), backend/ (FastAPI), docker-compose.yml
- Spec-Driven Development: EVERY implementation MUST start from and reference specs (@specs/features/task-crud.md, @specs/api/rest-endpoints.md, @specs/database/schema.md, etc.). Update specs first if anything is missing or unclear. No direct code generation without spec alignment.
- No manual coding allowed: All code changes are generated via agents/skills only. Review outputs strictly.
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS. Prefer server components. Client components only for interactivity. Use /lib/api.ts for all backend calls.
- Backend: Python FastAPI + SQLModel ORM. Routes under /api/. Use Pydantic for request/response models. HTTPException for errors.
- Database: Neon Serverless PostgreSQL. Connection via DATABASE_URL env. Models in backend/models.py. Enforce timestamps, indexes (user_id, completed).
- Authentication: Better Auth (frontend) with JWT plugin enabled. Shared secret via BETTER_AUTH_SECRET env var. Backend MUST verify JWT independently using PyJWT or equivalent → extract user_id → enforce strict user isolation on EVERY database query and route. No data leak possible. Return 401 Unauthorized if no/invalid token.
- API Endpoints: Stick exactly to documented endpoints (/api/{user_id}/tasks for list/create, /api/{user_id}/tasks/{id} for get/update/delete, PATCH /api/{user_id}/tasks/{id}/complete). All require valid JWT. Filter responses by authenticated user_id matching path user_id.
- Security & Quality:
  - User isolation mandatory: every task operation checks ownership via user_id from JWT.
  - Input validation: title 1-200 chars required, description ≤1000 chars optional.
  - Error handling: Global handlers in backend, proper UX feedback (toasts) in frontend.
  - Responsiveness: All UI must be mobile-friendly (Tailwind responsive classes).
  - Testing mindset: Favor testable code (small functions, dependencies injectable).
  - Performance: Use indexes, avoid N+1 queries in SQLModel.
  - Clean code: Follow PEP8 in Python, ESLint/Prettier style in TS/Next.js. Meaningful names, no duplication.
- Workflow priorities:
  1. Read/update relevant spec first.
  2. Generate plan (via plan-full-feature skill or main-agent).
  3. Delegate to specialized agents/skills (backend-agent, frontend-agent, etc.).
  4. Implement → review → test → integrate (docker-compose).
  5. Iterate only via spec changes if requirements evolve.
- Prohibited: Hard-coded secrets, bypassing auth, global state abuse, inline styles in frontend, raw SQL without SQLModel.

Constitution goals:
- Ensure consistent, secure, maintainable, multi-user Todo app.
- Guide agents to produce high-quality, production-ready code.
- Enforce spec-first discipline for hackathon judging (process, prompts, iterations visible).

## Response

I've created a comprehensive constitution for the Todo Full-Stack Web Application based on the project context you provided. The constitution includes:

- Six core principles covering spec-first development, agent-based implementation, security requirements, technology stack adherence, API contract compliance, and quality standards
- Additional constraints for technology stack, security, and performance
- Development workflow with process priorities, review process, and quality gates
- Governance section outlining how the constitution applies to the project

The constitution is now in place at `.specify/memory/constitution.md` and will guide all future development activities for the Todo Full-Stack Web Application project.