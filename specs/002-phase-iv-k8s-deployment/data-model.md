# Data Model: Phase IV Kubernetes Deployment

**Feature**: 002-phase-iv-k8s-deployment
**Date**: 2026-02-23
**Purpose**: Define Kubernetes entities and their relationships

---

## Key Entities

### 1. Docker Image

**What it represents**: Containerized application artifact

**Attributes**:
- `name`: Image name (e.g., `todo-backend`, `todo-frontend`)
- `tag`: Version tag (e.g., `latest`, `v1.0.0`)
- `base_image`: Base image (e.g., `python:3.11-alpine`, `node:20-alpine`)
- `size`: Final image size in MB
- `health_check`: Health check endpoint path
- `port`: Exposed port number

**Validation Rules**:
- Must use multi-stage build
- Must have non-root user
- Must have health check instruction
- Size must be under 300MB (frontend) or 200MB (backend)

---

### 2. Helm Chart

**What it represents**: Kubernetes package definition

**Attributes**:
- `name`: Chart name (e.g., `todo-frontend`, `todo-backend`)
- `version`: Chart version (e.g., `1.0.0`)
- `appVersion`: Application version
- `dependencies`: List of chart dependencies
- `templates`: List of Kubernetes resource templates

**Templates**:
- `deployment.yaml`: Pod deployment with replicas
- `service.yaml`: Network service definition
- `configmap.yaml`: Non-sensitive configuration
- `secrets.yaml`: Sensitive configuration (template only)
- `hpa.yaml`: Horizontal Pod Autoscaler (optional)
- `ingress.yaml`: Ingress routing (optional)

---

### 3. Kubernetes Deployment

**What it represents**: Desired state for application pods

**Attributes**:
- `name`: Deployment name
- `replicas`: Number of pod replicas
- `selector`: Label selector for pods
- `container`: Container specification
  - `image`: Container image reference
  - `ports`: List of exposed ports
  - `env`: Environment variables
  - `resources`: CPU/memory requests and limits
  - `livenessProbe`: Health check for pod restart
  - `readinessProbe`: Health check for traffic routing
  - `securityContext`: Security settings (non-root, read-only FS)

**Validation Rules**:
- Must have resource limits defined
- Must have liveness and readiness probes
- Must use specific image tag (not `latest` in production)
- Must run as non-root user

---

### 4. Kubernetes Service

**What it represents**: Network access pattern for pods

**Attributes**:
- `name`: Service name
- `type`: Service type (ClusterIP, NodePort, LoadBalancer)
- `selector`: Label selector for target pods
- `ports`: Port mappings
  - `port`: Service port
  - `targetPort`: Container port
  - `nodePort`: Node port (for NodePort/LoadBalancer)

**Types**:
- `ClusterIP`: Internal cluster access only
- `NodePort`: External access via node IP
- `LoadBalancer`: External access via load balancer (cloud)

---

### 5. Kubernetes ConfigMap

**What it represents**: Non-sensitive configuration data

**Attributes**:
- `name`: ConfigMap name
- `data`: Key-value pairs of configuration

**Configuration Keys**:
- `ENVIRONMENT`: Deployment environment (development/production)
- `LOG_LEVEL`: Logging verbosity (info/debug/error)
- `FRONTEND_URL`: Frontend service URL
- `BACKEND_URL`: Backend service URL

---

### 6. Kubernetes Secret

**What it represents**: Sensitive configuration data (base64 encoded)

**Attributes**:
- `name`: Secret name
- `type`: Secret type (Opaque, kubernetes.io/tls, etc.)
- `data`: Key-value pairs of base64-encoded secrets

**Secret Keys**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `COHERE_API_KEY`: Cohere LLM API key
- `BETTER_AUTH_SECRET`: Better Auth session secret
- `JWT_SECRET_KEY`: JWT signing secret

**Security Rules**:
- Never commit actual secret values to version control
- Use environment variables or external secrets manager
- Access controlled via RBAC

---

### 7. Helm Values

**What it represents**: Configurable parameters for Helm charts

**Structure**:
```yaml
# Common values
replicaCount: 2
image:
  repository: todo-app
  tag: "1.0.0"
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
  LOG_LEVEL: "info"

secrets:
  DATABASE_URL: "${DATABASE_URL}"
  COHERE_API_KEY: "${COHERE_API_KEY}"

service:
  type: NodePort
  port: 80
  targetPort: 3000
  nodePort: 30080

healthCheck:
  path: "/health"
  initialDelaySeconds: 30
  periodSeconds: 10
```

**Environment-Specific Overrides**:
- `values/dev.yaml`: Development environment
- `values/prod.yaml`: Production environment

---

### 8. Minikube Cluster

**What it represents**: Local Kubernetes cluster

**Attributes**:
- `driver`: Cluster driver (docker, virtualbox, etc.)
- `cpus`: Number of CPUs allocated
- `memory`: Amount of RAM allocated (MB)
- `addons`: Enabled addons (ingress, metrics-server, dashboard)
- `kubernetesVersion`: Kubernetes version

**Configuration**:
```bash
minikube start \
  --driver=docker \
  --cpus=4 \
  --memory=4096 \
  --addons=ingress,metrics-server,dashboard
```

---

## Entity Relationships

```
┌─────────────────┐
│  Docker Image   │
│  (todo-backend) │
└────────┬────────┘
         │ referenced by
         ▼
┌─────────────────┐
│   Deployment    │
│  (todo-backend) │
└────────┬────────┘
         │ creates
         ▼
┌─────────────────┐      selects     ┌─────────────────┐
│      Pods       │◄─────────────────│     Service     │
│  (todo-backend) │                  │  (todo-backend) │
└─────────────────┘                  └─────────────────┘
         │                                   │
         │ uses                              │ exposes
         ▼                                   ▼
┌─────────────────┐                  ┌─────────────────┐
│   ConfigMap     │                  │   NodePort:     │
│   (app-config)  │                  │  minikube-ip    │
└─────────────────┘                  └─────────────────┘
         │
         │ uses
         ▼
┌─────────────────┐
│     Secret      │
│  (app-secrets)  │
└─────────────────┘
```

---

## State Transitions

### Pod Lifecycle

1. **Pending**: Pod accepted by cluster, containers not yet created
2. **Pulling**: Container images being downloaded
3. **Running**: Containers running and healthy
4. **Failed**: Containers terminated with error
5. **Succeeded**: Containers completed successfully (for jobs)

**Desired State**: All pods in `Running` state with `1/1` containers ready

### Deployment Rollout

1. **Initial**: No replicas running
2. **Rolling Update**: New pods created, old pods terminated gradually
3. **Complete**: All replicas updated and healthy
4. **Failed**: Rollout stalled or failed (manual intervention needed)

---

## Validation Rules Summary

### Docker Images
- [ ] Multi-stage build
- [ ] Non-root user
- [ ] Health check instruction
- [ ] Size under limit (frontend <300MB, backend <200MB)

### Deployments
- [ ] Resource limits defined
- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Security context (non-root)
- [ ] Specific image tag (not `latest`)

### Services
- [ ] Correct port mappings
- [ ] Proper selector labels
- [ ] Appropriate service type for access pattern

### ConfigMaps/Secrets
- [ ] All required configuration keys present
- [ ] Secrets not committed to version control
- [ ] Proper base64 encoding for secrets

### Helm Charts
- [ ] Chart.yaml with metadata
- [ ] values.yaml with configurable parameters
- [ ] All templates use values (no hardcoded values)
- [ ] Templates pass `helm lint`

---

## Next Steps

Use these entities to generate:
1. Helm chart templates in `k8s/charts/`
2. Kubernetes manifests (if needed) in `k8s/manifests/`
3. Environment-specific values in `k8s/values/`
