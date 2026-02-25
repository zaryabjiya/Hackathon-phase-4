# Phase 0 Research: Phase IV Kubernetes Deployment

**Feature**: 002-phase-iv-k8s-deployment
**Date**: 2026-02-23
**Purpose**: Resolve all technical unknowns and establish best practices for Phase IV deployment

---

## Research Findings

### Decision 1: Containerization Strategy (Gordon AI)

**What was chosen**: Gordon (Docker AI Agent) for generating production-ready Dockerfiles

**Rationale**: 
- Phase IV constitution mandates AI-assisted containerization
- Gordon understands context and generates optimized multi-stage builds
- Reduces manual Dockerfile writing errors
- Ensures best practices (non-root users, health checks, lean images)

**Alternatives considered**:
- Manual Dockerfile writing → Rejected: Violates constitution Rule 2
- Standard Docker CLI → Rejected: Gordon provides AI optimization
- Other AI tools → Rejected: Gordon is Docker Desktop native

---

### Decision 2: Kubernetes Package Management (Helm)

**What was chosen**: Helm Charts for frontend and backend deployment

**Rationale**:
- Industry standard for Kubernetes packaging
- Enables versioned, repeatable deployments
- Configurable via values.yaml (dev/prod environments)
- Supports rollback and upgrade operations
- Constitution Rule 5 mandates Helm charts

**Alternatives considered**:
- Raw Kubernetes YAML → Rejected: Hard to manage, no templating
- Kustomize → Rejected: Less mature than Helm, team familiarity
- Skaffold → Rejected: More for development, Helm better for deployment

---

### Decision 3: Local Kubernetes (Minikube)

**What was chosen**: Minikube with Docker driver

**Rationale**:
- Zero-cost local development (constitution requirement)
- Production-like Kubernetes environment
- Easy setup and teardown
- Built-in dashboard for debugging
- Supports all required addons (ingress, metrics-server)

**Alternatives considered**:
- kind (Kubernetes in Docker) → Rejected: Minikube has better dashboard
- Docker Desktop Kubernetes → Rejected: Less configurable, no addons
- k3d → Rejected: Minikube more mature for local development

---

### Decision 4: AI DevOps Tools

**What was chosen**: kubectl-ai for K8s operations, kagent for analysis

**Rationale**:
- Constitution Rules 3 & 4 mandate AI-assisted K8s operations
- kubectl-ai generates YAML from natural language
- kagent provides cluster health analysis and optimization
- Reduces manual YAML writing (constitution requirement)

**Alternatives considered**:
- Manual kubectl → Rejected: Violates constitution
- Other AI tools → Rejected: kubectl-ai is purpose-built for K8s

---

### Decision 5: Environment Configuration

**What was chosen**: Kubernetes Secrets + ConfigMaps via Helm values

**Rationale**:
- Secrets for sensitive data (DATABASE_URL, API keys, auth secrets)
- ConfigMaps for non-sensitive configuration
- Helm manages both via values.yaml
- Never commit secrets to version control
- Constitution Rule 8 mandates proper env configuration

**Alternatives considered**:
- Environment variables in deployment YAML → Rejected: Not secure
- External secrets manager → Rejected: Overkill for local deployment
- .env files in containers → Rejected: Not Kubernetes-native

---

### Decision 6: Resource Limits

**What was chosen**: Conservative limits for local development

**Frontend**:
- Requests: 128Mi memory, 100m CPU
- Limits: 256Mi memory, 200m CPU

**Backend**:
- Requests: 256Mi memory, 200m CPU
- Limits: 512Mi memory, 500m CPU

**Rationale**:
- Minikube has limited resources (typically 2-4 CPU, 4-8GB RAM)
- Conservative limits prevent resource starvation
- Allows 2-3 replicas per service
- Can be adjusted based on actual usage

---

### Decision 7: Health Check Endpoints

**What was chosen**: HTTP health check endpoints

**Backend**: `/health` and `/ready` endpoints on port 8000
**Frontend**: `/health` endpoint on port 3000 (Next.js health check)

**Rationale**:
- Kubernetes native health check mechanism
- Enables automatic pod restart on failure
- Readiness probes prevent traffic to unready pods
- Constitution mandates health checks

---

### Decision 8: Service Exposure

**What was chosen**: NodePort for Minikube, Ingress optional

**Frontend**: NodePort (accessible via `minikube service`)
**Backend**: ClusterIP (internal only, accessed via frontend)

**Rationale**:
- NodePort simplest for local Minikube access
- Backend doesn't need external exposure (frontend proxies)
- Ingress optional for production-like routing
- Can add Ingress later if needed

---

### Decision 9: Image Build Strategy

**What was chosen**: Local Docker build, no container registry needed

**Rationale**:
- Minikube can use local Docker images with `minikube image load`
- No need for remote registry (Docker Hub, GCR) for local deployment
- Faster iteration (no push/pull)
- Zero cost (constitution requirement)

---

### Decision 10: Folder Structure

**What was chosen**:
```
todo-phs-iv/
├── docker/           # Dockerfiles, .dockerignore
├── k8s/
│   ├── charts/       # Helm charts (frontend, backend)
│   └── values/       # Environment-specific values
├── specs/phase-iv/   # Documentation
└── scripts/          # Deployment scripts
```

**Rationale**:
- Clear separation of Docker and Kubernetes artifacts
- Helm charts organized by service
- Environment-specific values for dev/prod
- Aligns with constitution folder structure

---

## Best Practices Established

### Docker Multi-Stage Builds
- Stage 1: Dependencies/build
- Stage 2: Production runtime
- Result: Lean production images

### Security
- Non-root users in all containers
- No secrets in version control
- Kubernetes Secrets for sensitive data
- Network policies (optional for local)

### Observability
- Minikube dashboard for visual monitoring
- `kubectl logs` for application logs
- `kubectl describe` for resource status
- kagent for cluster health analysis

### AI-Assisted Workflow
1. Gordon → Dockerfiles, .dockerignore
2. kubectl-ai → Helm charts, deployments
3. kagent → Analysis, optimization
4. Review all AI-generated content before applying

---

## Unresolved Issues

**None** - All technical unknowns resolved through research and constitution alignment.

---

## Next Steps

Proceed to Phase 1: Design & Contracts
- Create data-model.md (Kubernetes entities)
- Generate Helm chart contracts
- Create quickstart.md for deployment
