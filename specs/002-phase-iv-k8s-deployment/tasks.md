# Tasks: Phase IV Kubernetes Deployment

**Input**: Design documents from `/specs/002-phase-iv-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL for this deployment-focused feature. Implementation tasks are prioritized over test tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at repository root
- **Kubernetes resources**: `k8s/` directory
- **Docker resources**: `docker/` directory
- **Scripts**: `scripts/` directory
- **Documentation**: `specs/002-phase-iv-k8s-deployment/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project structure initialization and .gitignore updates

- [x] T001 Create docker/ directory structure per plan.md
- [x] T002 Create k8s/ directory structure with charts/, values/, manifests/ subdirectories
- [x] T003 Create scripts/ directory for deployment scripts
- [x] T004 Update root .gitignore to include docker/, k8s/, scripts/ directories
- [x] T005 [P] Create .gitkeep files in k8s/charts/, k8s/values/, k8s/manifests/

**Checkpoint**: ✅ Directory structure ready - proceed to Foundational phase

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Verify Docker Desktop is installed and running
- [ ] T007 [P] Enable Gordon (Docker AI) in Docker Desktop Settings → Beta Features
- [ ] T008 Verify Minikube is installed with `minikube version`
- [ ] T009 Verify Helm is installed with `helm version`
- [ ] T010 Verify kubectl is installed with `kubectl version --client`
- [ ] T011 [P] Install kubectl-ai (if not present) per quickstart.md
- [ ] T012 [P] Install kagent (if not present) per quickstart.md
- [ ] T013 Create .env.example with all required variables (DATABASE_URL, COHERE_API_KEY, BETTER_AUTH_SECRET, JWT_SECRET_KEY)
- [ ] T014 Verify backend/ has all Phase III dependencies (requirements.txt)
- [ ] T015 Verify frontend/ has all Phase III dependencies (package.json)

**Checkpoint**: Foundation ready - all tools installed, user story implementation can now begin in parallel

---

## Phase 3: User Story 2 - Containerized Applications with Production Dockerfiles (Priority: P1) 🎯

**Goal**: Generate production-ready Dockerfiles for frontend and backend using Gordon (Docker AI)

**Independent Test**: Can be fully tested by building Docker images locally using `docker build` and verifying they run correctly with `docker run` before any Kubernetes deployment

### Implementation for User Story 2

- [ ] T016 [P] [US2] Generate backend Dockerfile using Gordon in backend/Dockerfile
  - Command: `cd backend && docker ai "generate production-ready multi-stage Dockerfile for FastAPI backend with Python 3.11, virtual environment, non-root user, health check endpoint, lean alpine base"`
- [ ] T017 [P] [US2] Generate frontend Dockerfile using Gordon in frontend/Dockerfile
  - Command: `cd frontend && docker ai "generate production-ready multi-stage Dockerfile for Next.js 16+ with Node.js alpine, dependency caching, non-root user, health check"`
- [ ] T018 [P] [US2] Generate backend .dockerignore using Gordon in backend/.dockerignore
  - Command: `cd backend && docker ai "create .dockerignore for FastAPI Python backend"`
- [ ] T019 [P] [US2] Generate frontend .dockerignore using Gordon in frontend/.dockerignore
  - Command: `cd frontend && docker ai "create .dockerignore for Next.js frontend"`
- [ ] T020 [US2] Review and validate backend Dockerfile (multi-stage, non-root user, health check)
- [ ] T021 [US2] Review and validate frontend Dockerfile (multi-stage, non-root user, health check)
- [ ] T022 [US2] Build backend Docker image: `docker build -t todo-backend:latest .`
- [ ] T023 [US2] Build frontend Docker image: `docker build -t todo-frontend:latest .`
- [ ] T024 [US2] Test backend container locally: `docker run -p 8000:8000 todo-backend`
- [ ] T025 [US2] Test frontend container locally: `docker run -p 3000:3000 todo-frontend`
- [ ] T026 [US2] Verify health endpoints respond (backend: /health, frontend: /health)
- [ ] T027 [US2] Verify images are under size limits (backend <200MB, frontend <300MB)

**Checkpoint**: At this point, User Story 2 should be fully functional - both applications containerized and tested locally

---

## Phase 4: User Story 3 - Helm Charts for Repeatable Deployment (Priority: P1) 🎯

**Goal**: Generate Helm charts for frontend and backend using kubectl-ai for repeatable deployments

**Independent Test**: Can be fully tested by running `helm install` commands and verifying all Kubernetes resources are created correctly

### Implementation for User Story 3

- [ ] T028 [P] [US3] Create backend Helm chart structure using kubectl-ai in k8s/charts/todo-backend/
  - Command: `kubectl-ai "create a Helm chart for FastAPI backend deployment with 2 replicas, resource limits (512Mi memory, 500m CPU), health checks on /health endpoint, environment variables for DATABASE_URL and API keys"`
- [ ] T029 [P] [US3] Create frontend Helm chart structure using kubectl-ai in k8s/charts/todo-frontend/
  - Command: `kubectl-ai "create a Helm chart for Next.js frontend deployment with 2 replicas, resource limits (256Mi memory, 200m CPU), health checks on /health endpoint, NodePort service on port 3000"`
- [ ] T030 [US3] Review backend Chart.yaml (name, version, appVersion, description)
- [ ] T031 [US3] Review frontend Chart.yaml (name, version, appVersion, description)
- [ ] T032 [US3] Review backend values.yaml (replicas, resources, env, service, healthCheck)
- [ ] T033 [US3] Review frontend values.yaml (replicas, resources, env, service, healthCheck)
- [ ] T034 [US3] Verify backend templates/deployment.yaml (replicas, resources, probes, securityContext)
- [ ] T035 [US3] Verify frontend templates/deployment.yaml (replicas, resources, probes, securityContext)
- [ ] T036 [US3] Verify backend templates/service.yaml (ClusterIP, port 8000)
- [ ] T037 [US3] Verify frontend templates/service.yaml (NodePort, port 3000, nodePort 30080)
- [ ] T038 [P] [US3] Create k8s/values/dev.yaml with development environment values
- [ ] T039 [P] [US3] Create k8s/values/prod.yaml with production environment values (optional)
- [ ] T040 [US3] Run helm lint on backend chart: `helm lint ./k8s/charts/todo-backend`
- [ ] T041 [US3] Run helm lint on frontend chart: `helm lint ./k8s/charts/todo-frontend`
- [ ] T042 [US3] Run helm template on backend: `helm template todo-backend ./k8s/charts/todo-backend`
- [ ] T043 [US3] Run helm template on frontend: `helm template todo-frontend ./k8s/charts/todo-frontend`

**Checkpoint**: At this point, User Story 3 should be fully functional - Helm charts created, validated, and ready for deployment

---

## Phase 5: User Story 1 - Deploy Application to Local Kubernetes (Priority: P1) 🎯

**Goal**: Deploy the complete application to Minikube Kubernetes cluster using Helm

**Independent Test**: Can be fully tested by running `minikube start` followed by Helm install commands, and verifying all pods are running and application is accessible

### Implementation for User Story 1

- [ ] T044 [P] [US1] Start Minikube cluster: `minikube start --driver=docker --cpus=4 --memory=4096 --addons=ingress,metrics-server,dashboard`
- [ ] T045 [US1] Verify Minikube is running: `minikube status`
- [ ] T046 [US1] Verify kubectl is configured: `kubectl cluster-info`
- [ ] T047 [P] [US1] Load backend Docker image into Minikube: `minikube image load todo-backend:latest`
- [ ] T048 [P] [US1] Load frontend Docker image into Minikube: `minikube image load todo-frontend:latest`
- [ ] T049 [US1] Create Kubernetes secrets for sensitive data:
  ```
  kubectl create secret generic todo-secrets \
    --from-literal=DATABASE_URL="postgresql://..." \
    --from-literal=COHERE_API_KEY="..." \
    --from-literal=BETTER_AUTH_SECRET="..." \
    --from-literal=JWT_SECRET_KEY="..."
  ```
- [ ] T050 [US1] Install backend Helm chart: `helm install todo-backend ./k8s/charts/todo-backend --set image.repository=todo-backend --set image.tag=latest`
- [ ] T051 [US1] Install frontend Helm chart: `helm install todo-frontend ./k8s/charts/todo-frontend --set image.repository=todo-frontend --set image.tag=latest --set service.nodePort=30080`
- [ ] T052 [US1] Verify pods are running: `kubectl get pods`
- [ ] T053 [US1] Verify services are created: `kubectl get services`
- [ ] T054 [US1] Check pod logs for errors: `kubectl logs deployment/todo-backend`
- [ ] T055 [US1] Check pod logs for errors: `kubectl logs deployment/todo-frontend`
- [ ] T056 [US1] Describe backend deployment: `kubectl describe deployment todo-backend`
- [ ] T057 [US1] Describe frontend deployment: `kubectl describe deployment todo-frontend`
- [ ] T058 [US1] Access frontend via Minikube: `minikube service todo-frontend --url`
- [ ] T059 [US1] Verify frontend loads in browser at http://<minikube-ip>:30080

**Checkpoint**: At this point, User Story 1 should be fully functional - application deployed and accessible on Minikube

---

## Phase 6: User Story 5 - Preserve Phase III Functionality (Priority: P1) 🎯

**Goal**: Verify all Phase III features work correctly after Kubernetes deployment

**Independent Test**: Can be fully tested by using the chatbot via natural language commands after deployment and verifying tasks are added/listed/completed correctly

### Implementation for User Story 5

- [ ] T060 [US5] Test user authentication flow (register/login)
- [ ] T061 [US5] Test chat endpoint accessibility from frontend
- [ ] T062 [US5] Test natural language task creation: "Add task buy milk tomorrow"
- [ ] T063 [US5] Test natural language task listing: "Show my pending tasks"
- [ ] T064 [US5] Test natural language task completion: "Complete task 1"
- [ ] T065 [US5] Test natural language task deletion: "Delete task 1" (with confirmation)
- [ ] T066 [US5] Test natural language task update: "Update task 2 title to new title"
- [ ] T067 [US5] Verify MCP tools are functional (add_task, list_tasks, complete_task, delete_task, update_task)
- [ ] T068 [US5] Verify user isolation (users can only see their own tasks)
- [ ] T069 [US5] Verify JWT authentication is working
- [ ] T070 [US5] Verify database connection to Neon PostgreSQL is stable
- [ ] T071 [US5] Verify conversation history is persisted
- [ ] T072 [US5] Verify Roman Urdu + English responses are working
- [ ] T073 [US5] Test 50 task operations to verify database stability

**Checkpoint**: At this point, User Story 5 should be fully functional - all Phase III features working on Kubernetes

---

## Phase 7: User Story 4 - AI-Assisted DevOps Workflow (Priority: P2)

**Goal**: Verify and document AI-assisted workflow using Gordon, kubectl-ai, and kagent

**Independent Test**: Can be verified by reviewing command history showing Gordon used for Dockerfiles, kubectl-ai for K8s resources, and kagent for analysis

### Implementation for User Story 4

- [ ] T074 [P] [US4] Run kagent cluster health analysis: `kagent "analyze the cluster health"`
- [ ] T075 [US4] Review kagent recommendations for optimization
- [ ] T076 [P] [US4] Run kagent resource optimization: `kagent "optimize resource allocation for todo apps"`
- [ ] T077 [US4] Apply kagent recommendations (if any)
- [ ] T078 [P] [US4] Use kubectl-ai for debugging: `kubectl-ai "check why pod is crashing and fix it"` (if needed)
- [ ] T079 [US4] Use kubectl-ai for scaling: `kubectl-ai "scale todo-backend to 3 replicas"` (optional)
- [ ] T080 [US4] Document all AI prompts used in README
- [ ] T081 [US4] Create AI prompts reference section in documentation

**Checkpoint**: At this point, User Story 4 should be verified - AI-assisted workflow documented and functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, optimization, and final cleanup

- [ ] T082 [P] Update README.md with Phase IV deployment instructions
- [ ] T083 [P] Add quickstart section to README (reference quickstart.md)
- [ ] T084 [P] Add AI prompts reference to README (Gordon, kubectl-ai, kagent commands)
- [ ] T085 [P] Add troubleshooting section to README
- [ ] T086 Create deployment script scripts/minikube-deploy.sh (or .bat for Windows)
- [ ] T087 [P] Update specs/002-phase-iv-k8s-deployment/quickstart.md with any lessons learned
- [ ] T088 Run kagent final analysis: `kagent "analyze cluster health and suggest final optimizations"`
- [ ] T089 Verify resource utilization is within limits (frontend: 256Mi/200m, backend: 512Mi/500m)
- [ ] T090 Clean up unused Docker images: `docker image prune`
- [ ] T091 Verify all success criteria from spec.md are met (SC-001 through SC-010)
- [ ] T092 Create Phase IV completion summary document

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 2 (Phase 3)**: Containerization - Can start after Foundational, should complete before US1 and US3
- **User Story 3 (Phase 4)**: Helm Charts - Can start after Foundational, should complete before US1
- **User Story 1 (Phase 5)**: Deployment - Depends on US2 (Dockerfiles) and US3 (Helm charts) completion
- **User Story 5 (Phase 6)**: Phase III Preservation - Depends on US1 (deployment) completion
- **User Story 4 (Phase 7)**: AI Workflow - Can run in parallel with US5, but needs deployment complete
- **Polish (Phase 8)**: Depends on all user stories being substantially complete

### User Story Dependencies

- **User Story 2 (P1)**: Dockerfiles - Can start after Foundational - No dependencies on other stories
- **User Story 3 (P1)**: Helm Charts - Can start after Foundational - No dependencies on other stories
- **User Story 1 (P1)**: Deployment - Depends on US2 (images) and US3 (charts) - MVP story
- **User Story 5 (P1)**: Phase III Preservation - Depends on US1 (deployment complete)
- **User Story 4 (P2)**: AI Workflow - Can start after US1, runs parallel to US5

### Within Each User Story

- Dockerfiles before image builds (US2)
- Helm chart creation before lint/template validation (US3)
- Minikube start before Helm install (US1)
- Deployment before functionality testing (US5)
- AI analysis before applying optimizations (US4)

### Parallel Opportunities

- **Setup phase**: T001-T005 can all run in parallel (different directories)
- **Foundational phase**: T007, T011, T012 can run in parallel (different tool installations)
- **US2 (Containerization)**: T016-T019 (Gordon commands) can run in parallel (backend vs frontend)
- **US3 (Helm Charts)**: T028-T029 (backend vs frontend charts) can run in parallel
- **US1 (Deployment)**: T047-T048 (image loading) can run in parallel
- **Polish phase**: T082-T085 (documentation updates) can run in parallel

---

## Parallel Execution Examples

### User Story 2: Containerization (Parallel Dockerfiles)

```bash
# Terminal 1 - Backend
cd backend
docker ai "generate production-ready multi-stage Dockerfile for FastAPI backend"
docker ai "create .dockerignore for FastAPI Python backend"

# Terminal 2 - Frontend
cd frontend
docker ai "generate production-ready multi-stage Dockerfile for Next.js"
docker ai "create .dockerignore for Next.js frontend"
```

### User Story 3: Helm Charts (Parallel Chart Creation)

```bash
# Terminal 1 - Backend Chart
kubectl-ai "create a Helm chart for FastAPI backend deployment with 2 replicas, resource limits, health checks"

# Terminal 2 - Frontend Chart
kubectl-ai "create a Helm chart for Next.js frontend deployment with 2 replicas, NodePort service"
```

### User Story 1: Deployment (Parallel Image Loading)

```bash
# Terminal 1 - Backend Image
minikube image load todo-backend:latest

# Terminal 2 - Frontend Image
minikube image load todo-frontend:latest
```

---

## Implementation Strategy

### MVP First (User Story 2 + User Story 3 + User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 2 (Dockerfiles + images)
4. Complete Phase 4: User Story 3 (Helm charts)
5. Complete Phase 5: User Story 1 (Deploy to Minikube)
6. **STOP and VALIDATE**: Verify pods running, frontend accessible
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Tools ready
2. Add User Story 2 → Dockerfiles ready → Test locally
3. Add User Story 3 → Helm charts ready → Validate with lint/template
4. Add User Story 1 → Deploy to Minikube → Test accessibility (MVP!)
5. Add User Story 5 → Verify Phase III functionality → Full validation
6. Add User Story 4 → AI workflow optimization → Polish
7. Complete Polish phase → Documentation complete

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 2 (Containerization)
   - Developer B: User Story 3 (Helm Charts)
3. Both complete → Developer A+B: User Story 1 (Deployment together)
4. Developer A: User Story 5 (Functionality testing)
5. Developer B: User Story 4 (AI workflow + optimization)
6. Team: Polish phase together

---

## Task Summary

| Phase | User Story | Task Count | Priority |
|-------|-----------|------------|----------|
| 1 | Setup | 5 | - |
| 2 | Foundational | 10 | - |
| 3 | US2: Containerization | 12 | P1 |
| 4 | US3: Helm Charts | 16 | P1 |
| 5 | US1: Deployment | 16 | P1 |
| 6 | US5: Phase III Preservation | 14 | P1 |
| 7 | US4: AI Workflow | 8 | P2 |
| 8 | Polish | 11 | - |

**Total Tasks**: 92

**Parallel Opportunities**:
- Setup phase: 5 tasks can run in parallel
- Foundational phase: 3 tasks can run in parallel
- US2: 4 Gordon tasks can run in parallel (backend vs frontend)
- US3: 2 chart creation tasks can run in parallel
- US1: 2 image loading tasks can run in parallel
- Polish phase: 4 documentation tasks can run in parallel

**Suggested MVP Scope**: Phases 1-5 (Setup, Foundational, US2, US3, US1) = 59 tasks
- Dockerfiles generated and tested locally
- Helm charts created and validated
- Application deployed to Minikube and accessible

**Full Implementation**: All 8 phases = 92 tasks

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [US1], [US2], etc. labels map task to specific user story for traceability
- Verify all AI-generated content (Dockerfiles, Helm charts) before applying
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All commands assume Windows environment (adjust for Linux/Mac as needed)
- Gordon, kubectl-ai, kagent must be installed and configured before starting
