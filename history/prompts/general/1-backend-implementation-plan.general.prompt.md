---
id: 1
title: Backend Implementation Plan
stage: general
date_iso: 2026-02-13
surface: agent
model: Qwen
feature: none
branch: main
user: system
command: /sp.plan Create a DETAILED, BACKEND-ONLY implementation plan for completing the entire backend of the Todo Full-Stack Web Application (Phase II), based strictly on the latest backend specifications
labels: ["backend", "implementation", "plan", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - D:\hackathon\todo-phs-ii\specs\impl-plan.backend.md
tests_yaml: []
---

# Prompt History Record

## PROMPT_TEXT

$ARGUMENTS

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.plan Create a DETAILED, BACKEND-ONLY implementation plan for completing the entire backend of the Todo Full-Stack Web Application (Phase II), based strictly on the latest backend specifications (from specs/api/rest-endpoints.md, specs/database/schema.md, specs/features/authentication.md, specs/features/task-crud.md, specs/api/backend-integration.md).

IMPORTANT CONSTRAINTS:
- This plan is 100% backend-focused. DO NOT include, mention, plan, or delegate ANY frontend-related tasks (Next.js pages, components, Tailwind, TypeScript UI, auth client-side).
- Treat the frontend as an existing client at http://localhost:3000 that will call the API with JWT Bearer tokens.
- Use exactly these env vars from .env:
  - BETTER_AUTH_SECRET=aPwV1FM8W5bmHF7o7xCgsq5PDACVaNFO
  - DATABASE_URL=postgresql://neondb_owner:npg_W5vTSROKo4ZJ@ep-small-base-a70deu8b-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
- Goal: Secure, production-ready FastAPI backend with JWT auth, Neon PostgreSQL persistence, strict user isolation, and full CRUD for tasks.

Plan Structure Requirements:
1. High-Level Overview
   - Summary of backend deliverables
   - Key milestones (e.g., DB setup → Auth integration → Task routes → Middleware & security → Testing)

2. Phased Implementation Steps (numbered 1–N, 8–12 phases recommended)
   For each phase:
   - Phase name & goal
   - Dependencies (previous phases or specs to read)
   - Specific files/folders to create or modify (with exact paths, e.g. backend/main.py, backend/models.py)
   - Key features/techniques to implement (e.g., SQLModel async session, JWT middleware, Pydantic models, ownership checks)
   - Which agent/skill to delegate to (use your existing ones: backend-agent, jwt-fastapi-middleware, sqlmodel-task-model, tasks-crud-routes-fastapi, error-handling-global, test-crud-endpoints, etc.)
   - Estimated complexity (low/medium/high)
   - Acceptance criteria (what "done" looks like, e.g. "All routes return 401 without token, 403 on wrong user_id")

3. Delegation Table
   - Markdown table summarizing:
     | Phase # | Task Description                          | Delegate To (agent/skill)      | Priority | Files Involved                  |

4. Prerequisites & Setup Reminders
   - Required packages to install (pip install fastapi sqlmodel uvicorn better-auth pyjwt pydantic python-dotenv alembic if migrations needed)
   - .env loading in main.py (from dotenv import load_dotenv; load_dotenv())
   - Neon DB connection: Use SQLModel.create_engine with DATABASE_URL, handle SSL params correctly

5. Security & Integration Phase
   - JWT verification middleware: Verify signature with BETTER_AUTH_SECRET, extract user_id, attach to request.state.user
   - User isolation enforcement: In every DB query → .where(Task.user_id == current_user.id)
   - Better Auth server integration: Mount auth routes (/api/auth/*), enable JWT plugin on server side

6. Testing & Validation Phase
   - Manual testing checklist (curl/postman for each endpoint with/without token, wrong user_id, invalid data)
   - Pytest suggestions (test_tasks.py for CRUD + auth failures)
   - Integration check: Run backend + frontend together, test sign-in → tasks fetch

7. Output Format
   - Clean markdown
   - Use tables, checklists, code blocks for file paths & commands
   - End with next action: "After this plan is approved, start delegation with phase 1 using main-agent or backend-agent. Then run: cd backend && uvicorn main:app --reload --port 8000"

Prioritize order logically:
1. Project setup & dependencies
2. .env loading & DB connection
3. SQLModel models & schema creation
4. Better Auth server setup with JWT plugin
5. JWT verification middleware / dependency
6. Task CRUD routes with user isolation
7. Error handling & validation
8. Logging & CORS (allow frontend origin http://localhost:3000)
9. Testing & final security checks

Ensure EVERY backend requirement from the spec is covered: user_id matching, input validation (title 1-200, desc ≤1000), timestamps, indexes, 401/403 responses, etc.

## RESPONSE_TEXT

I've created a detailed backend-only implementation plan for the Todo Full-Stack Web Application (Phase II). The plan includes:

1. High-Level Overview with deliverables and milestones
2. 10 Phased Implementation Steps covering everything from project setup to final validation
3. A delegation table mapping phases to appropriate agents/skills
4. Prerequisites and setup reminders with required packages
5. Security and integration phase details
6. Testing and validation phase with checklist
7. Output format with file structure and commands

The plan follows all constraints:
- 100% backend-focused with no frontend tasks
- Uses the exact environment variables specified
- Covers all required endpoints and security measures
- Includes proper user isolation and validation
- Details JWT middleware implementation
- Outlines testing and validation steps

The implementation plan is saved in D:\hackathon\todo-phs-ii\specs\impl-plan.backend.md and is ready for execution.

## OUTCOME

Created a comprehensive backend implementation plan that covers all required functionality while adhering to the constraints of being backend-only and using the specified environment variables and technologies.

## EVALUATION

The plan successfully addresses all requirements in the prompt, including the phased approach, delegation strategy, security considerations, and proper file structure. It's ready for execution by the appropriate agents.