# Helm Chart Contracts

**Feature**: 002-phase-iv-k8s-deployment
**Date**: 2026-02-23
**Purpose**: Define Helm chart structure and API contracts

---

## Backend Helm Chart Contract

### Chart.yaml
```yaml
apiVersion: v2
name: todo-backend
description: FastAPI Backend for Todo AI Chatbot
type: application
version: 1.0.0
appVersion: "3.0.0"
keywords:
  - fastapi
  - python
  - backend
  - todo
  - ai
maintainers:
  - name: Phase IV Team
```

### values.yaml (Default)
```yaml
replicaCount: 2

image:
  repository: todo-backend
  tag: "latest"
  pullPolicy: IfNotPresent

resources:
  requests:
    memory: "256Mi"
    cpu: "200m"
  limits:
    memory: "512Mi"
    cpu: "500m"

env:
  ENVIRONMENT: "development"
  LOG_LEVEL: "info"

secrets:
  DATABASE_URL: ""
  COHERE_API_KEY: ""
  BETTER_AUTH_SECRET: ""
  JWT_SECRET_KEY: ""

service:
  type: ClusterIP
  port: 8000
  targetPort: 8000

healthCheck:
  path: "/health"
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

podAnnotations: {}

nodeSelector: {}

tolerations: []

affinity: {}
```

### Expected Templates

#### deployment.yaml
- Must create Deployment with specified replicas
- Must include resource limits and requests
- Must configure liveness and readiness probes
- Must mount secrets as environment variables
- Must use non-root security context

#### service.yaml
- Must create ClusterIP service (default)
- Must expose port 8000
- Must select pods with correct labels

#### configmap.yaml
- Must contain non-sensitive environment variables
- Must be mounted as environment variables in pods

#### secrets.yaml (template)
- Must reference external Kubernetes secrets
- Must not contain actual secret values in chart

---

## Frontend Helm Chart Contract

### Chart.yaml
```yaml
apiVersion: v2
name: todo-frontend
description: Next.js Frontend for Todo AI Chatbot
type: application
version: 1.0.0
appVersion: "3.0.0"
keywords:
  - nextjs
  - react
  - frontend
  - todo
  - ai
maintainers:
  - name: Phase IV Team
```

### values.yaml (Default)
```yaml
replicaCount: 2

image:
  repository: todo-frontend
  tag: "latest"
  pullPolicy: IfNotPresent

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"

env:
  ENVIRONMENT: "development"
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"

service:
  type: NodePort
  port: 80
  targetPort: 3000
  nodePort: 30080

healthCheck:
  path: "/health"
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

podAnnotations: {}

nodeSelector: {}

tolerations: []

affinity: {}
```

### Expected Templates

#### deployment.yaml
- Must create Deployment with specified replicas
- Must include resource limits and requests
- Must configure liveness and readiness probes
- Must configure environment variables
- Must use non-root security context

#### service.yaml
- Must create NodePort service (default for Minikube)
- Must expose port 80, targetPort 3000
- Must use configurable nodePort (default 30080)
- Must select pods with correct labels

#### configmap.yaml
- Must contain non-sensitive environment variables
- Must include NEXT_PUBLIC_API_URL for backend connection

---

## Umbrella Chart Contract (Optional)

### Chart.yaml
```yaml
apiVersion: v2
name: todo-app
description: Umbrella Helm Chart for Todo AI Chatbot
type: application
version: 1.0.0
appVersion: "3.0.0"
dependencies:
  - name: todo-frontend
    version: 1.0.0
    repository: "file://../todo-frontend"
  - name: todo-backend
    version: 1.0.0
    repository: "file://../todo-backend"
```

### values.yaml
```yaml
todo-frontend:
  replicaCount: 2
  service:
    type: NodePort
    nodePort: 30080

todo-backend:
  replicaCount: 2
  service:
    type: ClusterIP
```

---

## Validation Rules

### helm lint
```bash
helm lint ./k8s/charts/backend
helm lint ./k8s/charts/frontend
```

**Expected**: No errors, warnings allowed

### helm template
```bash
helm template todo-backend ./k8s/charts/backend
helm template todo-frontend ./k8s/charts/frontend
```

**Expected**: Valid Kubernetes YAML output

### helm install --dry-run
```bash
helm install todo-backend ./k8s/charts/backend --dry-run
helm install todo-frontend ./k8s/charts/frontend --dry-run
```

**Expected**: Installation succeeds in dry-run mode

---

## Upgrade Strategy

### Backend Upgrade
```bash
helm upgrade todo-backend ./k8s/charts/backend \
  --set image.tag=v1.0.1 \
  --rolling-update
```

### Frontend Upgrade
```bash
helm upgrade todo-frontend ./k8s/charts/frontend \
  --set image.tag=v1.0.1 \
  --rolling-update
```

### Rollback
```bash
helm rollback todo-backend
helm rollback todo-frontend
```

---

## Versioning Policy

- **MAJOR**: Breaking API changes, database schema changes
- **MINOR**: New features, backward-compatible additions
- **PATCH**: Bug fixes, performance improvements

Chart version follows semantic versioning (MAJOR.MINOR.PATCH)
