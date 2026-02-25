---
id: 27
title: create-cohere-implementation-tasks
stage: tasks
date: 2026-02-18
surface: agent
model: qwen-code
feature: 001-cohere-multi-agent
branch: 001-cohere-multi-agent
user: AK C0M
command: /sp.tasks
labels: ["tasks", "phase-iii", "cohere", "multi-agent", "chatbot", "implementation", "breakdown"]
links:
  spec: specs/001-cohere-multi-agent/spec.md
  plan: specs/001-cohere-multi-agent/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-cohere-multi-agent/tasks.md
tests:
  - Task format validation (checkbox, ID, story label, file path)
  - User story organization (5 stories mapped)
  - Dependency order verified (Setup → Foundational → Stories → Polish)
tests_yaml:
  - Task count per phase validation
  - Parallel opportunities identified
  - Independent test criteria for each story
  - MVP scope defined (User Story 1 only)
---

## Prompt

---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
handoffs: 
  - label: Analyze For Consistency
    agent: sp.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: sp.implement
    prompt: Start the implementation in phases
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: 

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label  
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

---

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

## Response snapshot

Implementation tasks created successfully for Cohere Multi-Agent Todo System:

**Tasks File**: `specs/001-cohere-multi-agent/tasks.md`

**Task Summary**:
- **Total Tasks**: 94 tasks
- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 8 tasks
- **Phase 3 (US1 - Add Task)**: 19 tasks
- **Phase 4 (US2 - List Tasks)**: 12 tasks
- **Phase 5 (US3 - Complete/Update)**: 12 tasks
- **Phase 6 (US4 - Context)**: 10 tasks
- **Phase 7 (US5 - Delete)**: 9 tasks
- **Phase 8 (Polish)**: 19 tasks

**MVP Scope** (User Story 1 Only): 32 tasks (Phases 1-3)
**Full Feature Scope**: 94 tasks (All phases)

**Format Validation**: ✅ PASS
- All tasks follow checklist format: `- [ ] T### [P?] [US#] Description with file path`
- All user story phases have [US#] labels
- Setup, Foundational, and Polish phases have NO story labels
- All tasks include exact file paths
- Sequential task IDs (T001-T094)

**Parallel Opportunities Identified**:
- Phase 1: T002, T003, T005 (dependency installation)
- Phase 2: T007, T008, T009, T012 (migrations, auth, contracts)
- Phase 3 (US1): T014, T015, T016 (server, tools, agent)
- Phase 4 (US2): T033, T034, T035 (list_tasks tool, queries)
- Phase 5 (US3): T045, T046, T047 (complete/update tools)
- Phase 6 (US4): T057, T058 (history loading)
- Phase 7 (US5): T067, T068 (delete tool)
- Phase 8: Most polish tasks can run in parallel

**Independent Test Criteria** (per story):
- **US1**: "Add task buy milk" → task created with confirmation
- **US2**: "Show pending tasks" → formatted list with 🕒 emojis
- **US3**: "Complete task 3" → task marked complete with confirmation
- **US4**: "What are my tasks?" → "Complete the first one" → context understood
- **US5**: "Delete task 5" → "Pakka delete karun?" → confirmation flow

**Implementation Strategy**:
1. **MVP First**: Complete Phases 1-3 (32 tasks) → Users can add tasks conversationally
2. **Incremental Delivery**: Add one user story at a time, test independently
3. **Parallel Team**: After Foundational, split US1-3 across 3 developers

**Next Steps**:
- Start with T001 (Create .env file)
- Complete Phase 2 (Foundational) before ANY user story work
- Implement US1 (T014-T032) for MVP demo
- Validate each story independently at phase checkpoints

## Outcome

- ✅ Impact: Complete, actionable task breakdown for Cohere Multi-Agent Todo System (94 tasks)
- 🧪 Tests: Format validation passed, all tasks have file paths and story labels
- 📁 Files: 1 created (tasks.md with full implementation breakdown)
- 🔁 Next prompts: Run `/sp.implement` to start Phase 1 implementation
- 🧠 Reflection: Tasks successfully organized by user story for independent implementation and testing

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation completed successfully
- Graders run and results: N/A (task list, no code tests)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with T001 (Setup phase)
