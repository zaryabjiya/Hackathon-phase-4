# Tasks: Cohere Multi-Agent Todo System

**Input**: Design documents from `/specs/001-cohere-multi-agent/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Tests**: Tests are OPTIONAL - not included in this task list (TDD not requested)
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at repository root
- Paths based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend/.env file with COHERE_API_KEY, BETTER_AUTH_SECRET, DATABASE_URL, JWT_SECRET_KEY
- [X] T002 [P] Install backend dependencies: cohere, mcp, sqlmodel, fastapi, uvicorn[standard], asyncpg in backend/requirements.txt
- [ ] T003 [P] Install frontend dependency: @openai/chatkit in frontend/package.json
- [X] T004 Create backend/mcp/__init__.py and backend/agents/__init__.py
- [X] T005 [P] Update .gitignore to exclude .env and .env.local files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create backend/models/conversation.py with Conversation and Message SQLModel classes
- [X] T007 Create backend/migrations/add_conversations_messages.py Alembic migration for conversations and messages tables
- [X] T008 [P] Create indexes: ix_conversations_user_id, ix_messages_conversation_id, ix_messages_created_at
- [X] T009 [P] Verify backend/lib/auth.py has get_current_user dependency for JWT verification
- [X] T010 Create backend/db/session.py with async get_db session manager
- [X] T011 Update backend/main.py to include router for /api/{user_id}/chat endpoint
- [X] T012 Create specs/001-cohere-multi-agent/contracts/mcp-tools.yaml with OpenAPI schemas for 5 MCP tools
- [X] T013 Update .env.example with COHERE_API_KEY and document all environment variables

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks using natural language commands ("Add task buy milk tomorrow")

**Independent Test**: User types "Add task buy milk tomorrow" → task created with title "buy milk" and due date "tomorrow"

### Implementation for User Story 1

- [X] T014 [P] [US1] Create backend/mcp/server.py with FastMCP("todo_mcp") server definition
- [X] T015 [P] [US1] Create backend/mcp/tools.py with add_task tool implementation (user_id, title, description)
- [X] T016 [P] [US1] Create backend/agents/todo_master.py with TodoMaster system prompt and Cohere client initialization
- [ ] T017 [US1] Implement Cohere tool calling in backend/agents/todo_master.py (parse tool_calls from response)
- [ ] T018 [US1] Create backend/routes/chat.py with POST /api/{user_id}/chat endpoint
- [ ] T019 [US1] Implement conversation creation logic in backend/routes/chat.py (new conversation for first message)
- [ ] T020 [US1] Save user message to messages table in backend/routes/chat.py
- [ ] T021 [US1] Load conversation history (last 20 messages) in backend/routes/chat.py
- [ ] T022 [US1] Call Cohere chat() with system prompt, history, and tools in backend/routes/chat.py
- [ ] T023 [US1] Execute add_task tool when Cohere returns tool_call in backend/routes/chat.py
- [ ] T024 [US1] Save assistant response with tool execution results to messages table
- [ ] T025 [US1] Return ChatResponse with response text and conversation_id
- [ ] T026 [US1] Add input validation: title 1-200 chars, description ≤1000 chars in backend/mcp/tools.py
- [ ] T027 [US1] Add logging for add_task operations (success/failure) in backend/mcp/tools.py
- [ ] T028 Create frontend/lib/api.ts with sendChatMessage function (POST to /api/{user_id}/chat)
- [ ] T029 Create frontend/app/page.tsx with ChatKit component integration
- [ ] T030 [US1] Configure ChatKit theme with primaryColor, backgroundColor, textColor in frontend/app/page.tsx
- [ ] T031 [US1] Handle JWT token from localStorage in frontend/app/page.tsx (Authorization header)
- [ ] T032 [US1] Save conversation_id to localStorage after first message in frontend/app/page.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently
- User can type "Add task buy milk" → task is created and confirmed

---

## Phase 4: User Story 2 - Conversational Task Listing (Priority: P1)

**Goal**: Users can view tasks through natural language queries ("Show pending tasks")

**Independent Test**: User types "Show pending tasks" → formatted list with 🕒 emojis appears

### Implementation for User Story 2

- [ ] T033 [P] [US2] Create backend/mcp/tools.py with list_tasks tool implementation (user_id, status filter)
- [ ] T034 [P] [US2] Add SQLModel query: select(Task).where(Task.user_id == user_id, Task.completed == False) for pending
- [ ] T035 [P] [US2] Add SQLModel query: select(Task).where(Task.user_id == user_id, Task.completed == True) for completed
- [ ] T036 [US2] Update backend/agents/todo_master.py system prompt to include list_tasks tool description
- [ ] T037 [US2] Implement list_tasks tool execution in backend/routes/chat.py when Cohere returns tool_call
- [ ] T038 [US2] Format task list response with numbered list and 🕒 emojis for pending tasks
- [ ] T039 [US2] Format completed tasks with ✓ checkmarks in response
- [ ] T040 [US2] Handle empty state: "Abhi koi task nahi hai! Naya shuru karen? 😄"
- [ ] T041 [US2] Add status_filter parameter support: "all", "pending", "completed" in backend/mcp/tools.py
- [ ] T042 [US2] Truncate long task titles (>50 chars) with "..." in list response
- [ ] T043 [US2] Show task descriptions (if available) on indented new line in list response
- [ ] T044 [US2] Add logging for list_tasks operations in backend/mcp/tools.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently
- User can add tasks AND view tasks conversationally

---

## Phase 5: User Story 3 - Task Completion & Updates (Priority: P2)

**Goal**: Users can mark tasks complete or update them through conversation

**Independent Test**: User types "Complete task 3" or "Update task 2 title to buy organic milk" → changes reflected

### Implementation for User Story 3

- [ ] T045 [P] [US3] Create backend/mcp/tools.py with complete_task tool implementation (user_id, task_id)
- [ ] T046 [P] [US3] Create backend/mcp/tools.py with update_task tool implementation (user_id, task_id, title, description)
- [ ] T047 [P] [US3] Add ownership verification: query Task with user_id AND task_id to prevent IDOR in backend/mcp/tools.py
- [ ] T048 [US3] Implement task not found error: "Task nahi mila... koi aur ID try karo? 😅" in backend/mcp/tools.py
- [ ] T049 [US3] Update task.completed = True and task.updated_at in complete_task tool
- [ ] T050 [US3] Update task.title or task.description in update_task tool
- [ ] T051 [US3] Return confirmation: "Task complete mark kar diya! Well done 🔥" in backend/mcp/tools.py
- [ ] T052 [US3] Return confirmation: "Task update ho gaya! ✏️" in backend/mcp/tools.py
- [ ] T053 [US3] Update backend/agents/todo_master.py system prompt to include complete_task and update_task tool descriptions
- [ ] T054 [US3] Implement complete_task and update_task tool execution in backend/routes/chat.py
- [ ] T055 [US3] Add validation: task_id must be positive integer in backend/mcp/tools.py
- [ ] T056 [US3] Add logging for complete_task and update_task operations in backend/mcp/tools.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently
- User can add, view, complete, and update tasks conversationally

---

## Phase 6: User Story 4 - Multi-Turn Conversation with Context (Priority: P2)

**Goal**: System remembers conversation context for natural back-and-forth dialogue

**Independent Test**: User asks "What are my tasks?" then says "Complete the first one" → system understands which task

### Implementation for User Story 4

- [ ] T057 [P] [US4] Update backend/routes/chat.py to load last 20 messages from conversation
- [ ] T058 [P] [US4] Convert messages to Cohere chat_history format: [{"role": "USER"/"CHATBOT", "message": "..."}]
- [ ] T059 [US4] Pass chat_history to Cohere chat() call in backend/routes/chat.py
- [ ] T060 [US4] Update backend/agents/todo_master.py system prompt to include context handling instructions
- [ ] T061 [US4] Implement context-aware greeting: "Hey [Name]! Kya plan hai aaj? Koi naya task add karen ya purane dekhen? 😊" for new conversations
- [ ] T062 [US4] Handle follow-up references: "the first one", "that task", "my tasks" in system prompt
- [ ] T063 [US4] Store conversation.title (auto-generate from first user message if "New Chat")
- [ ] T064 [US4] Update conversation.updated_at timestamp on each message in backend/routes/chat.py
- [ ] T065 [US4] Add logic to detect and handle ambiguous references (ask clarification question)
- [ ] T066 [US4] Test context retention across 20+ message exchanges

**Checkpoint**: At this point, User Stories 1-4 should all work with full conversation context

---

## Phase 7: User Story 5 - Task Deletion with Confirmation (Priority: P3)

**Goal**: Users can delete tasks with confirmation for destructive actions

**Independent Test**: User types "Delete task 5" → system asks "Pakka delete karun?" before proceeding

### Implementation for User Story 5

- [ ] T067 [P] [US5] Create backend/mcp/tools.py with delete_task tool implementation (user_id, task_id)
- [ ] T068 [P] [US5] Add ownership verification in delete_task: query Task with user_id AND task_id
- [ ] T069 [US5] Update backend/agents/todo_master.py system prompt to require confirmation before delete
- [ ] T070 [US5] Implement two-step delete flow:
  1. User: "Delete task 5" → Agent: "Pakka delete karun? (haan/na)"
  2. User: "haan" → Execute delete_task tool
  3. User: "na" → Cancel deletion
- [ ] T071 [US5] Track pending deletion state in conversation context (which task awaiting confirmation)
- [ ] T072 [US5] Return confirmation: "Task delete ho gaya! 🗑️" after successful deletion
- [ ] T073 [US5] Handle cancel: "Theek hai, task delete nahi kiya gaya 👍" in backend/agents/todo_master.py
- [ ] T074 [US5] Add logging for delete_task operations (success/failure/cancel) in backend/mcp/tools.py
- [ ] T075 [US5] Add soft delete option consideration (deleted_at field) vs hard delete in backend/models/task.py

**Checkpoint**: All 5 user stories should now be independently functional
- User can add, view, complete, update, and delete tasks conversationally with full context

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T076 [P] Create specs/001-cohere-multi-agent/quickstart.md with step-by-step setup guide
- [ ] T077 [P] Update README.md with Phase III features and ChatKit integration section
- [ ] T078 [P] Create docs/DEMO_SCRIPT.md with natural language examples for hackathon demo
- [ ] T079 [P] Add error handling for Cohere API timeouts in backend/routes/chat.py
- [ ] T080 [P] Add retry logic for database operations in backend/mcp/tools.py
- [ ] T081 [P] Implement rate limiting on /api/{user_id}/chat endpoint (60 requests/minute) in backend/routes/chat.py
- [ ] T082 [P] Add request/response logging middleware in backend/main.py
- [ ] T083 [P] Create backend/.env.example with all environment variables documented
- [ ] T084 [P] Create frontend/.env.local.example with NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- [ ] T085 [P] Add CORS middleware in backend/main.py for frontend domain
- [ ] T086 [P] Test full conversation flow: add → list → complete → update → delete
- [ ] T087 [P] Verify user isolation: User A cannot access User B's tasks (IDOR test)
- [ ] T088 [P] Test JWT expiration handling (401 Unauthorized response)
- [ ] T089 [P] Verify conversation history limit (last 20 messages) works correctly
- [ ] T090 [P] Performance test: p95 latency < 2 seconds for chat responses
- [ ] T091 [P] Mobile responsiveness test for ChatKit UI
- [ ] T092 [P] Add OpenAI ChatKit domain allowlist configuration to quickstart.md
- [ ] T093 [P] Create demo video script with 5-7 conversation flows
- [ ] T094 [P] Run constitution compliance check (all 8 gates) before final commit

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Benefits from US1-3 but independent
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Independent of other stories

### Within Each User Story

- Models before services (if applicable)
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T002, T003, T005 can run in parallel
- **Phase 2 (Foundational)**: T007, T008, T009, T012 can run in parallel
- **Phase 3 (US1)**: T014, T015, T016 can start in parallel (different files)
- **Phase 4 (US2)**: T033, T034, T035 can start in parallel
- **Phase 5 (US3)**: T045, T046, T047 can start in parallel
- **Phase 6 (US4)**: T057, T058 can start in parallel
- **Phase 7 (US5)**: T067, T068 can start in parallel
- **Phase 8 (Polish)**: Most tasks can run in parallel (different concerns)

---

## Parallel Example: User Story 1

```bash
# Launch all US1 model/tool creation tasks together:
Task: "T014 [P] [US1] Create backend/mcp/server.py with FastMCP server"
Task: "T015 [P] [US1] Create backend/mcp/tools.py with add_task tool"
Task: "T016 [P] [US1] Create backend/agents/todo_master.py with system prompt"

# After T014-T016 complete, continue with:
Task: "T017 [US1] Implement Cohere tool calling in todo_master.py"
Task: "T018 [US1] Create chat endpoint in routes/chat.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T013) - **CRITICAL BLOCKER**
3. Complete Phase 3: User Story 1 (T014-T032)
4. **STOP and VALIDATE**: Test "Add task buy milk" → task created
5. Deploy/demo if ready for MVP

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test: "Add task" works → Deploy/Demo (MVP!)
3. Add User Story 2 → Test: "Show tasks" works → Deploy/Demo
4. Add User Story 3 → Test: "Complete/Update task" works → Deploy/Demo
5. Add User Story 4 → Test: Context retention works → Deploy/Demo
6. Add User Story 5 → Test: Delete with confirmation works → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T013)
2. Once Foundational is done:
   - **Developer A**: User Story 1 (T014-T032) - Add task
   - **Developer B**: User Story 2 (T033-T044) - List tasks
   - **Developer C**: User Story 3 (T045-T056) - Complete/Update
3. After US1-3 complete:
   - **Developer A**: User Story 4 (T057-T066) - Context
   - **Developer B**: User Story 5 (T067-T075) - Delete
   - **Developer C**: Phase 8 Polish (T076-T094)
4. Stories complete and integrate independently

---

## Task Summary

| Phase | Description | Task Count | Story |
|-------|-------------|------------|-------|
| **Phase 1** | Setup | 5 tasks | - |
| **Phase 2** | Foundational | 8 tasks | - |
| **Phase 3** | User Story 1 (Add) | 19 tasks | US1 |
| **Phase 4** | User Story 2 (List) | 12 tasks | US2 |
| **Phase 5** | User Story 3 (Complete/Update) | 12 tasks | US3 |
| **Phase 6** | User Story 4 (Context) | 10 tasks | US4 |
| **Phase 7** | User Story 5 (Delete) | 9 tasks | US5 |
| **Phase 8** | Polish | 19 tasks | - |
| **Total** | **All phases** | **94 tasks** | **5 stories** |

### MVP Scope (User Story 1 Only)
- **Minimum**: Phases 1-3 (T001-T032) = **32 tasks**
- Users can add tasks via natural language

### Full Feature Scope
- **All phases**: T001-T094 = **94 tasks**
- Complete conversational todo management

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability (e.g., [US1], [US2])
- Each user story should be independently completable and testable
- Commit after each task or logical group (e.g., all US1 tools complete)
- Stop at checkpoints to validate story independently
- **CRITICAL**: Phase 2 (Foundational) MUST complete before ANY user story work
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Task IDs are sequential (T001-T094) for easy tracking
- File paths are absolute from repository root
