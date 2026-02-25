# Implementation Plan: Phase IV Kubernetes Deployment

**Branch**: `002-phase-iv-k8s-deployment` | **Date**: 2026-02-23 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-phase-iv-k8s-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy Phase III's fully working AI Todo Chatbot (Next.js frontend + FastAPI backend + Better Auth + Neon Postgres + MCP tools + ChatKit) to local Kubernetes cluster (Minikube) using Helm Charts, Docker (with Gordon AI), kubectl-ai, and kagent for AI-assisted DevOps workflow while preserving all Phase III functionality.

**Technical Approach**:
- Gordon (Docker AI) for production-ready multi-stage Dockerfiles
- kubectl-ai for Helm chart generation and Kubernetes operations
- kagent for cluster health analysis and optimization
- Helm charts for repeatable, configurable deployments
- Minikube for zero-cost local Kubernetes cluster
- Kubernetes Secrets and ConfigMaps for environment configuration

---

## Technical Context

**Language/Version**: Python 3.11 (Backend), Node.js 20 (Frontend)
**Primary Dependencies**: FastAPI, Next.js 16+, Better Auth, MCP SDK, Cohere API
**Storage**: Neon PostgreSQL (external serverless), Kubernetes Secrets/ConfigMaps
**Testing**: pytest (backend), Jest (frontend), helm lint/template (K8s)
**Target Platform**: Local Kubernetes (Minikube) with Docker driver
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**: 
  - Health checks respond within 2 seconds
  - All pods running within 5 minutes of deployment
  - Zero downtime during rolling updates
**Constraints**: 
  - Local deployment only (no cloud costs)
  - Minikube resource limits (4 CPU, 4GB RAM typical)
  - Docker images under 300MB (frontend), 200MB (backend)
**Scale/Scope**: 
  - 2 replicas per service (configurable)
  - Resource limits: Frontend 256Mi/200m, Backend 512Mi/500m
  - Support 10+ concurrent users for local testing

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase IV Constitution Compliance

| Constitution Rule | Compliance Status | Evidence |
|-------------------|-------------------|----------|
| Rule 1: Spec-Driven Development | ✅ PASS | Spec created at `specs/002-phase-iv-k8s-deployment/spec.md` before plan |
| Rule 2: Gordon (Docker AI) First | ✅ PASS | All Dockerfiles generated via Gordon commands in quickstart.md |
| Rule 3: kubectl-ai for K8s | ✅ PASS | All Helm charts and K8s resources via kubectl-ai commands |
| Rule 4: kagent for Analysis | ✅ PASS | kagent commands included for cluster health and optimization |
| Rule 5: Helm Charts Mandatory | ✅ PASS | Separate Helm charts for frontend and backend in contracts |
| Rule 6: Local Minikube Deployment | ✅ PASS | Minikube with Docker driver, zero-cost local setup |
| Rule 7: Phase III Preservation | ✅ PASS | All Phase III functionality (chat, MCP tools, auth, DB) preserved |
| Rule 8: Environment Configuration | ✅ PASS | Kubernetes Secrets and ConfigMaps for all env vars |

### Gate Evaluation

**Result**: ✅ PASS - All constitution rules satisfied with zero violations

**Justification**:
- AI-assisted workflow enforced throughout (Gordon, kubectl-ai, kagent)
- No manual YAML/Dockerfile writing (all AI-generated)
- Phase III functionality explicitly preserved in spec requirements
- Zero-cost local deployment via Minikube
- Proper secrets management via Kubernetes Secrets

---

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-iv-k8s-deployment/
├── plan.md              # This file
├── research.md          # Phase 0 output (all unknowns resolved)
├── data-model.md        # Phase 1 output (K8s entities)
├── quickstart.md        # Phase 1 output (deployment guide)
├── contracts/           # Phase 1 output
│   └── helm-charts.md   # Helm chart API contracts
└── tasks.md             # Phase 2 output (NOT created by /sp.plan)
```

### Source Code (repository root)

```text
todo-phs-iv/
├── backend/
│   ├── src/
│   ├── Dockerfile                   # Gordon-generated
│   ├── .dockerignore                # Gordon-generated
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   ├── Dockerfile                   # Gordon-generated
│   ├── .dockerignore                # Gordon-generated
│   ├── package.json
│   └── .env
├── docker/                          # NEW: Docker configurations
│   └── docker-compose.yml           # Optional: local testing
├── k8s/                             # NEW: Kubernetes resources
│   ├── charts/
│   │   ├── todo-frontend/           # kubectl-ai generated
│   │   │   ├── Chart.yaml
│   │   │   ├── values.yaml
│   │   │   └── templates/
│   │   ├── todo-backend/            # kubectl-ai generated
│   │   │   ├── Chart.yaml
│   │   │   ├── values.yaml
│   │   │   └── templates/
│   │   └── todo-umbrella/           # Optional: combined chart
│   └── values/
│       ├── dev.yaml
│       └── prod.yaml
├── specs/
│   └── 002-phase-iv-k8s-deployment/ # This feature
├── scripts/                         # NEW: Deployment scripts
│   └── minikube-deploy.sh
├── history/
│   ├── prompts/
│   └── adr/
├── .env.example
├── docker-compose.yml
├── README.md
└── SETUP_GUIDE.md
```

**Structure Decision**: Web application structure with separate `backend/` and `frontend/` directories, plus new `k8s/` and `docker/` directories for Phase IV deployment artifacts. This matches the existing Phase II/III monorepo structure.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. Constitution Check passed with all rules compliant.

---

## Phase 0: Research Summary

**Status**: ✅ COMPLETE

All technical unknowns resolved in `research.md`:

1. ✅ Containerization strategy (Gordon AI)
2. ✅ Kubernetes package management (Helm)
3. ✅ Local Kubernetes (Minikube)
4. ✅ AI DevOps tools (kubectl-ai, kagent)
5. ✅ Environment configuration (Secrets + ConfigMaps)
6. ✅ Resource limits (conservative for local)
7. ✅ Health check endpoints (HTTP /health, /ready)
8. ✅ Service exposure (NodePort for Minikube)
9. ✅ Image build strategy (local Docker, no registry)
10. ✅ Folder structure (docker/, k8s/, charts/)

**No unresolved issues**. Proceed to Phase 1.

---

## Phase 1: Design & Contracts Summary

**Status**: ✅ COMPLETE

### Artifacts Created

1. **data-model.md**: Kubernetes entities defined
   - Docker Image, Helm Chart, Deployment, Service
   - ConfigMap, Secret, Helm Values, Minikube Cluster
   - Entity relationships and validation rules

2. **contracts/helm-charts.md**: Helm chart API contracts
   - Backend chart structure (FastAPI)
   - Frontend chart structure (Next.js)
   - Umbrella chart (optional)
   - Validation rules (helm lint, template, install --dry-run)

3. **quickstart.md**: Step-by-step deployment guide
   - Prerequisites checklist
   - 10-step quick start (5 minutes)
   - Debugging commands
   - Common issues and solutions
   - AI prompts reference

### Agent Context Update

**New Technologies to Add**:
- Minikube (local Kubernetes)
- Helm (package manager)
- kubectl-ai (AI K8s operations)
- kagent (cluster analysis)
- Gordon (Docker AI Agent)

**Action**: Run update-agent-context script to add these tools to agent knowledge base.

---

## Phase 2 Planning Readiness

**Constitution Check Re-evaluation**: ✅ PASS (post-design)

All design artifacts align with constitution:
- AI-assisted workflow (Gordon, kubectl-ai, kagent)
- No manual YAML writing
- Phase III functionality preserved
- Zero-cost local deployment
- Proper secrets management

**Ready for `/sp.tasks`**: Yes

---

## Implementation Roadmap

### Step 1: Update Project Structure (10 minutes)
- Create `docker/`, `k8s/`, `scripts/` directories
- Update `.gitignore` for new folders
- Create `k8s/.gitkeep` files

**AI Commands**: None (manual setup)

**Success Criteria**: Directory structure matches plan

---

### Step 2: Generate Dockerfiles with Gordon (20 minutes)
- Backend Dockerfile (FastAPI)
- Frontend Dockerfile (Next.js)
- Backend .dockerignore
- Frontend .dockerignore

**AI Commands**:
```bash
cd backend
docker ai "generate production-ready multi-stage Dockerfile for FastAPI backend"

cd ../frontend
docker ai "generate production-ready multi-stage Dockerfile for Next.js"
```

**Success Criteria**: 
- Multi-stage builds
- Non-root users
- Health checks
- Images under size limits

---

### Step 3: Local Docker Testing (15 minutes)
- Build backend image
- Build frontend image
- Test containers locally

**Commands**:
```bash
docker build -t todo-backend:latest .
docker build -t todo-frontend:latest .
docker run -p 8000:8000 todo-backend
docker run -p 3000:3000 todo-frontend
```

**Success Criteria**: 
- Images build without errors
- Health endpoints respond
- Containers run as non-root

---

### Step 4: Minikube Setup (10 minutes)
- Start Minikube with addons
- Verify kubectl configuration
- Enable dashboard

**Commands**:
```bash
minikube start --driver=docker --cpus=4 --memory=4096 --addons=ingress,metrics-server,dashboard
kubectl cluster-info
```

**Success Criteria**: 
- Minikube running
- All addons enabled
- kubectl configured

---

### Step 5: Generate Helm Charts with kubectl-ai (30 minutes)
- Backend Helm chart
- Frontend Helm chart
- Optional umbrella chart

**AI Commands**:
```bash
kubectl-ai "create Helm chart for FastAPI backend with 2 replicas, resource limits, health checks"
kubectl-ai "create Helm chart for Next.js frontend with NodePort service"
```

**Success Criteria**: 
- Chart.yaml, values.yaml, templates created
- `helm lint` passes
- `helm template` produces valid YAML

---

### Step 6: Deploy to Minikube (15 minutes)
- Create Kubernetes secrets
- Install backend Helm chart
- Install frontend Helm chart
- Verify pods running

**Commands**:
```bash
kubectl create secret generic todo-secrets --from-literal=...
helm install todo-backend ./k8s/charts/backend
helm install todo-frontend ./k8s/charts/frontend
kubectl get pods
```

**Success Criteria**: 
- All pods Running (1/1 ready)
- Services created
- No crash loops

---

### Step 7: Verification & Testing (20 minutes)
- Access frontend via Minikube IP
- Test chatbot functionality
- Verify MCP tools working
- Check authentication

**Commands**:
```bash
minikube service todo-frontend --url
# Test: "Add task buy milk"
# Test: "Show my tasks"
```

**Success Criteria**: 
- Frontend accessible
- Chatbot responds
- Tasks CRUD working
- Auth functioning

---

### Step 8: Documentation Update (30 minutes)
- Update README with Phase IV instructions
- Add AI prompts used
- Create deployment guide
- Document troubleshooting

**Success Criteria**: 
- README has complete deployment steps
- All AI prompts documented
- Troubleshooting section included

---

### Step 9: Final Cleanup & Optimization (15 minutes)
- Run kagent analysis
- Optimize resource allocation
- Clean up unused images
- Verify resource usage

**AI Commands**:
```bash
kagent "analyze cluster health and suggest optimizations"
kagent "optimize resource allocation for todo apps"
```

**Success Criteria**: 
- Resources within limits
- No wasted capacity
- Cluster healthy

---

## Total Time Estimate

- **First-time setup**: 2.5 - 3 hours
- **Subsequent deployments**: 30-45 minutes
- **With automation scripts**: 10-15 minutes

---

## Next Steps

1. Run `/sp.tasks` to break this plan into actionable tasks
2. Execute tasks in sequence (or parallel where marked [P])
3. Create PHR after each major milestone
4. Update README with deployment guide

---

**Plan Status**: ✅ COMPLETE - Ready for task breakdown via `/sp.tasks`
