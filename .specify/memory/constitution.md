<!--
Sync Impact Report:
Version change: 2.0.0 → 3.0.0 (MAJOR: Phase IV Kubernetes Deployment with AI-assisted DevOps)
Modified principles:
  - PROJECT OVERVIEW → Phase IV: Local Kubernetes Deployment context
  - CORE OBJECTIVE → Containerization + Helm + Minikube deployment
  - NON-NEGOTIABLE RULES → 8 rules for K8s deployment + AI tool usage
  - TECHNOLOGY STACK → Minikube, Helm, Gordon, kubectl-ai, kagent
  - AI TOOLS USAGE → Gordon, kubectl-ai, kagent guidelines
  - GOVERNANCE → Phase IV deployment compliance
Added sections:
  - FOLDER STRUCTURE (Phase IV additions: helm/, k8s/, docker/)
  - DEPLOYMENT PRINCIPLES (Zero-cost, production-like local)
  - CONTAINERIZATION STANDARDS (Multi-stage Dockerfiles)
  - HELM CHART REQUIREMENTS (Frontend/Backend charts)
  - KUBERNETES RESOURCE GUIDELINES (Replicas, ports, services)
  - AI-ASSISTED DEVOPS WORKFLOW (Gordon/kubectl-ai/kagent commands)
  - LOCAL CLUSTER OPERATIONS (Minikube dashboard, debugging)
  - ENVIRONMENT CONFIGURATION (K8s env vars, secrets management)
  - PREVIOUS PHASES INTEGRATION (Phase III functionality preservation)
Removed sections:
  - CORE IDENTITY & PERSONALITY (TodoMaster - not relevant for deployment phase)
  - CHAT ENDPOINT FLOW (implementation detail, not deployment concern)
  - STARTING MESSAGE (UI concern, not deployment)
  - EXAMPLE BEHAVIORS (chatbot-specific, not deployment)
Templates requiring updates:
  - ⚠ .specify/templates/plan-template.md (pending - needs K8s Constitution Check)
  - ⚠ .specify/templates/spec-template.md (pending - needs deployment spec structure)
  - ⚠ .specify/templates/tasks-template.md (pending - needs K8s task types)
Follow-up TODOs:
  - TODO(TEMPLATE_SYNC): Update plan-template.md Constitution Check for Phase IV K8s requirements
  - TODO(TEMPLATE_SYNC): Update spec-template.md for deployment spec structure (Helm, containers)
  - TODO(TEMPLATE_SYNC): Update tasks-template.md for K8s deployment tasks (containerize, helm, deploy)
  - TODO(MONITORING): Add observability section for K8s monitoring (Prometheus/Grafana optional)
-->

# Todo AI Chatbot - Phase IV Constitution (Kubernetes Deployment Edition)

## Version & Governance

**Version**: 3.0.0
**Ratified**: 2026-02-13
**Last Amended**: 2026-02-23
**Phase**: IV (Local Kubernetes Deployment)
**Deployment Target**: Minikube (Local K8s Cluster)
**Containerization**: Docker Desktop + Gordon (Docker AI Agent)
**Package Manager**: Helm Charts
**AI DevOps Tools**: kubectl-ai, kagent

---

## 1. PROJECT OVERVIEW & INTEGRATION

Yeh Phase IV hai hackathon-todo project ka.  
Hum Phase III ke fully working AI Todo Chatbot (Next.js frontend + FastAPI backend + Better Auth + Neon Postgres + MCP tools + ChatKit) ko **local Kubernetes cluster** pe deploy kar rahe hain.

**Goal**: Zero-cost, production-like local deployment using modern Cloud-Native tools with heavy AI assistance.

**Previous Phases Integration**
- Phase I → Console Todo
- Phase II → Full-Stack Web (FastAPI + Next.js)
- Phase III → AI Chatbot with MCP tools
- **Phase IV → Kubernetes Deployment (Minikube + Helm + AI Agents)**

Sab kuch **same monorepo** (hackathon-todo/) mein rahega. Koi alag repo nahi.

---

## 2. CORE OBJECTIVE

Containerize frontend aur backend, Helm Charts banao, Minikube pe deploy karo, aur **kubectl-ai + kagent + Gordon** (Docker AI Agent) ka heavy use karke AI-assisted deployment karo.

**Non-Negotiable**:
- Har containerization step pe Gordon (Docker AI) ka use
- Har K8s resource generation pe kubectl-ai ka use
- Har optimization/analysis step pe kagent ka use
- Manual YAML writing sirf AI-generated content ko review karne ke baad

---

## 3. NON-NEGOTIABLE CONSTITUTION RULES

### Rule 1: Spec-Driven Development
Har cheez Spec-Driven rahegi (@specs/ folder use karo). Pehle spec, phir plan, phir tasks, phir implementation.

### Rule 2: Gordon (Docker AI) First
Containerization ke liye hamesha Gordon ko prioritize karo:
- `docker ai "containerize this Next.js frontend for production"`
- `docker ai "generate multi-stage Dockerfile for FastAPI backend"`
- `docker ai "create docker-compose.yml for local testing"`

### Rule 3: kubectl-ai for K8s Operations
Har Kubernetes operation AI se generate karwao:
- `kubectl-ai "deploy the todo frontend with 2 replicas and expose on port 3000"`
- `kubectl-ai "create Helm chart for backend service"`
- `kubectl-ai "check why pod is crashing and fix it"`

### Rule 4: kagent for Analysis
Advanced analysis aur optimization ke liye kagent use karo:
- `kagent "analyze the cluster health"`
- `kagent "optimize resource allocation for todo apps"`
- `kagent "suggest improvements for high availability"`

### Rule 5: Helm Charts Mandatory
Frontend aur backend ke alag Helm charts hone chahiye:
- `helm create todo-frontend`
- `helm create todo-backend`
- Optional: Umbrella chart for combined deployment

### Rule 6: Local Minikube Deployment
Deployment fully local Minikube pe hona chahiye:
- Zero cost (no cloud spending)
- Production-like environment
- Easy debugging via Minikube dashboard

### Rule 7: Phase III Functionality Preservation
All previous Phase III functionality working rahe:
- Chat endpoint with Cohere
- MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Better Auth JWT authentication
- Neon PostgreSQL connection
- User isolation (strict)

### Rule 8: Environment Configuration
Deployment fully environment variables se configure ho:
- `DATABASE_URL` (Neon connection string)
- `COHERE_API_KEY`
- `BETTER_AUTH_SECRET`
- `JWT_SECRET_KEY`
- K8s Secrets aur ConfigMaps ka proper use

---

## 4. TECHNOLOGY STACK (Phase IV Specific)

### Containerization
- **Docker Desktop**: Base containerization platform
- **Gordon (Docker AI Agent)**: AI-powered Dockerfile generation

### Orchestration
- **Kubernetes**: Container orchestration
- **Minikube**: Local K8s cluster

### Package Manager
- **Helm Charts**: Application packaging and deployment

### AI DevOps Assistants
- **kubectl-ai**: Natural language K8s operations
- **kagent**: Cluster analysis and optimization

### Base Applications
- **Frontend**: Next.js (Phase III)
- **Backend**: FastAPI (Phase III)

### Database
- **Neon PostgreSQL**: External serverless database
- Connection string via environment variables

### Monitoring & Debugging
- **Minikube Dashboard**: Built-in K8s UI
- **kubectl-ai/kagent**: AI-powered debugging

---

## 5. AI TOOLS USAGE GUIDELINES

### Gordon (Docker AI Agent)

**Enable First**:
```
Docker Desktop → Settings → Beta Features → Gordon on
```

**Standard Commands**:
```bash
docker ai "containerize this Next.js frontend for production"
docker ai "generate multi-stage Dockerfile for FastAPI backend"
docker ai "create docker-compose.yml for local testing"
docker ai "optimize this Dockerfile for smaller image size"
```

**Best Practices**:
- Always review AI-generated Dockerfiles
- Use multi-stage builds for production
- Keep images lean (alpine base where possible)
- Proper .dockerignore files

### kubectl-ai

**Standard Commands**:
```bash
kubectl-ai "deploy the todo frontend with 2 replicas and expose on port 3000"
kubectl-ai "create Helm chart for backend service"
kubectl-ai "check why pod is crashing and fix it"
kubectl-ai "create ingress for todo app"
kubectl-ai "setup horizontal pod autoscaler for backend"
```

**Best Practices**:
- Review generated YAML before applying
- Use `--dry-run` for validation
- Test in isolated namespace first
- Keep resource definitions version-controlled

### kagent

**Standard Commands**:
```bash
kagent "analyze the cluster health"
kagent "optimize resource allocation for todo apps"
kagent "suggest improvements for high availability"
kagent "identify security vulnerabilities in deployment"
```

**Best Practices**:
- Run kagent analysis before production-like tests
- Use recommendations for optimization
- Document decisions made from kagent suggestions

---

## 6. FOLDER STRUCTURE (Phase IV Additions)

```
todo-phs-iv/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # This file (Phase IV)
│   ├── templates/
│   │   ├── plan-template.md
│   │   ├── spec-template.md
│   │   ├── tasks-template.md
│   │   └── phr-template.prompt.md
│   └── scripts/
├── specs/
│   ├── 001-cohere-multi-agent/      # Phase III specs
│   ├── database/
│   ├── api/
│   └── phase-iv-k8s/                # NEW: Phase IV deployment specs
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── backend/
│   ├── src/
│   ├── Dockerfile                   # AI-generated (Gordon)
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   ├── Dockerfile                   # AI-generated (Gordon)
│   ├── package.json
│   └── .env
├── docker/                          # NEW: Docker configurations
│   ├── docker-compose.yml           # AI-generated
│   └── .dockerignore
├── helm/                            # NEW: Helm charts
│   ├── todo-frontend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   ├── todo-backend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   └── todo-umbrella/               # Optional: combined chart
│       ├── Chart.yaml
│       └── requirements.yaml
├── k8s/                             # NEW: Raw K8s manifests (if needed)
│   ├── namespaces/
│   ├── configmaps/
│   ├── secrets/
│   ├── deployments/
│   ├── services/
│   └── ingress/
├── history/
│   ├── prompts/
│   └── adr/
├── .env.example
├── docker-compose.yml
├── README.md
└── SETUP_GUIDE.md
```

---

## 7. DEPLOYMENT PRINCIPLES

### Zero-Cost Local Development
- No cloud spending required
- Minikube for local K8s cluster
- Docker Desktop for containerization
- Free tier tools only (Neon, Cohere free tier if available)

### Production-Like Environment
- Same environment as production (K8s)
- Proper resource limits and requests
- Health checks and readiness probes
- Proper logging and monitoring setup

### AI-Assisted Everything
- Gordon for Dockerfiles
- kubectl-ai for K8s resources
- kagent for optimization
- Manual work only when AI unavailable

### Incremental Deployment
1. Containerize backend → Test locally
2. Containerize frontend → Test locally
3. Create Helm charts → Test on Minikube
4. Deploy backend → Verify
5. Deploy frontend → Verify
6. Full integration test

---

## 8. CONTAINERIZATION STANDARDS

### Dockerfile Requirements
- Multi-stage builds mandatory
- Lean base images (alpine where possible)
- Proper .dockerignore files
- Non-root user for security
- Health check instructions
- Environment variable configuration

### Backend Dockerfile (FastAPI)
```dockerfile
# AI-generated via Gordon
# Must include:
# - Python slim/alpine base
# - Virtual environment setup
# - Dependency installation
# - Non-root user
# - Health check endpoint
# - Proper signal handling
```

### Frontend Dockerfile (Next.js)
```dockerfile
# AI-generated via Gordon
# Must include:
# - Node alpine base
# - Multi-stage build (build + production)
# - Proper caching of dependencies
# - Static asset optimization
# - Health check
```

---

## 9. HELM CHART REQUIREMENTS

### Chart Structure
```
todo-frontend/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    ├── ingress.yaml (optional)
    └── hpa.yaml (optional)
```

### Mandatory Templates
- **Deployment**: With replicas, resource limits, health probes
- **Service**: ClusterIP for internal, NodePort/LoadBalancer for external
- **ConfigMap**: Non-sensitive configuration
- **Secrets**: Sensitive data (via K8s secrets or external secrets manager)

### Values Configuration
- Image repository and tag
- Replica count
- Resource limits/requests
- Environment variables
- Service type and ports

---

## 10. KUBERNETES RESOURCE GUIDELINES

### Resource Limits
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### Health Probes
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Service Exposure
- **Backend**: ClusterIP (internal) + Ingress (external via API gateway)
- **Frontend**: NodePort (Minikube) or LoadBalancer (cloud)

### Ingress Configuration
- Single ingress for both frontend and backend
- Path-based routing:
  - `/` → Frontend
  - `/api/*` → Backend

---

## 11. LOCAL CLUSTER OPERATIONS

### Minikube Commands
```bash
# Start cluster
minikube start --driver=docker

# Enable dashboard
minikube dashboard

# Access service
minikube service todo-frontend

# View logs
kubectl logs -f deployment/todo-backend

# Debug pod
kubectl exec -it pod/todo-backend-xxx -- /bin/bash
```

### Debugging Workflow
1. Use Minikube dashboard for visual inspection
2. Use `kubectl logs` for application logs
3. Use `kubectl describe` for resource status
4. Use kubectl-ai for AI-powered debugging
5. Use kagent for cluster health analysis

---

## 12. ENVIRONMENT CONFIGURATION

### Kubernetes Secrets
```bash
# Create secrets
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=COHERE_API_KEY="..." \
  --from-literal=BETTER_AUTH_SECRET="..." \
  --from-literal=JWT_SECRET_KEY="..."
```

### ConfigMaps
```bash
# Create configmap
kubectl create configmap todo-config \
  --from-literal=ENVIRONMENT="production" \
  --from-literal=LOG_LEVEL="info"
```

### Helm Values Override
```yaml
# values-production.yaml
backend:
  env:
    DATABASE_URL: ${DATABASE_URL}
    COHERE_API_KEY: ${COHERE_API_KEY}
  resources:
    limits:
      memory: "512Mi"
      cpu: "500m"
```

---

## 13. PREVIOUS PHASES INTEGRATION

### Phase III Functionality Checklist
- ✅ Chat endpoint with Cohere working
- ✅ MCP tools functional (add_task, list_tasks, complete_task, delete_task, update_task)
- ✅ Better Auth JWT authentication
- ✅ Neon PostgreSQL connection
- ✅ User isolation (strict enforcement)
- ✅ Conversation history persistence
- ✅ Message history (last 20 messages)

### Database Schema (Unchanged)
- `tasks` table (Phase II)
- `conversations` table (Phase III)
- `messages` table (Phase III)

### API Endpoints (Preserved)
- `POST /api/{user_id}/chat` - Chat endpoint
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `GET /users/{user_id}/tasks` - List tasks
- `POST /users/{user_id}/tasks` - Create task
- `PUT /users/{user_id}/tasks/{task_id}` - Update task
- `DELETE /users/{user_id}/tasks/{task_id}` - Delete task

---

## 14. SAFETY & FINAL RULES

### Security
- Never commit `.env` files or secrets
- Use K8s secrets for sensitive data
- Non-root containers
- Network policies for pod isolation
- JWT validation on all authenticated endpoints

### Best Practices
- Always test locally before deployment
- Use Helm for repeatable deployments
- Version control all K8s manifests
- Document all AI-generated content
- Keep images updated (security patches)

### Final Rules
- Constitution compliance mandatory
- AI tools ka maximum use
- Zero-cost local deployment
- Phase III functionality preservation
- Spec-driven development

---

## GOVERNANCE

### Amendment Procedure
Constitution changes require:
1. Version bump (semantic versioning)
2. Sync Impact Report at top of file
3. Template updates if needed
4. User confirmation for MAJOR changes

### Versioning Policy
- **MAJOR**: Backward incompatible changes (Phase change, K8s removal, AI tool change)
- **MINOR**: New deployment features, new principles, material expansions
- **PATCH**: Clarifications, typo fixes, wording improvements

### Compliance Review
All PRs/reviews must verify:
- Constitution compliance
- AI tool usage (Gordon, kubectl-ai, kagent)
- Helm chart structure
- Phase III functionality preservation
- Security best practices
- Zero-cost deployment adherence

---

**Yeh constitution Phase IV ke liye complete hai** — sab cover ho gaya:
- ✅ Kubernetes deployment (Minikube)
- ✅ Containerization (Docker + Gordon)
- ✅ Helm Charts (Frontend + Backend)
- ✅ AI DevOps tools (kubectl-ai, kagent)
- ✅ Phase III functionality preservation
- ✅ Environment configuration
- ✅ Security best practices
- ✅ Local cluster operations
- ✅ Zero-cost deployment
