# Quickstart: Phase IV Kubernetes Deployment

**Feature**: 002-phase-iv-k8s-deployment
**Date**: 2026-02-23
**Purpose**: Step-by-step guide for deploying Phase IV on Minikube

---

## Prerequisites

Ensure you have the following installed:

- [ ] Docker Desktop (with Gordon enabled)
- [ ] Minikube
- [ ] Helm
- [ ] kubectl
- [ ] kubectl-ai (optional but recommended)
- [ ] kagent (optional but recommended)

---

## Quick Start (5 minutes)

### Step 1: Start Minikube

```bash
minikube start --driver=docker --cpus=4 --memory=4096 --addons=ingress,metrics-server,dashboard
```

**Expected Output**:
```
😄  minikube v1.32.0 on Microsoft Windows 11
✨  Using the docker driver based on existing profile
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image ...
🔥  Creating docker container (CPUs=4, Memory=4096MB) ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: ingress, metrics-server, dashboard
🏄  Done! kubectl is now configured to use "minikube" cluster
```

### Step 2: Generate Dockerfiles with Gordon

**Backend Dockerfile**:
```bash
cd backend
docker ai "generate a production-ready multi-stage Dockerfile for FastAPI backend with Python 3.11, virtual environment, non-root user, health check endpoint, and lean alpine base image"
```

**Frontend Dockerfile**:
```bash
cd ../frontend
docker ai "generate a production-ready multi-stage Dockerfile for Next.js 16+ with Node.js alpine, dependency caching, non-root user, health check, and lean production image"
```

### Step 3: Build Docker Images

**Backend**:
```bash
cd backend
docker build -t todo-backend:latest .
```

**Frontend**:
```bash
cd ../frontend
docker build -t todo-frontend:latest .
```

### Step 4: Load Images into Minikube

```bash
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### Step 5: Generate Helm Charts with kubectl-ai

**Backend Helm Chart**:
```bash
kubectl-ai "create a Helm chart for FastAPI backend deployment with 2 replicas, resource limits (512Mi memory, 500m CPU), health checks on /health endpoint, and environment variables for DATABASE_URL and API keys"
```

**Frontend Helm Chart**:
```bash
kubectl-ai "create a Helm chart for Next.js frontend deployment with 2 replicas, resource limits (256Mi memory, 200m CPU), health checks on /health endpoint, and NodePort service on port 3000"
```

### Step 6: Create Kubernetes Secrets

```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="postgresql://user:pass@neon.tech/dbname" \
  --from-literal=COHERE_API_KEY="your-cohere-api-key" \
  --from-literal=BETTER_AUTH_SECRET="your-better-auth-secret" \
  --from-literal=JWT_SECRET_KEY="your-jwt-secret"
```

### Step 7: Install Helm Charts

**Backend**:
```bash
helm install todo-backend ./k8s/charts/backend \
  --set secrets.DATABASE_URL=$(kubectl get secret todo-secrets -o jsonpath='{.data.DATABASE_URL}') \
  --set image.repository=todo-backend \
  --set image.tag=latest
```

**Frontend**:
```bash
helm install todo-frontend ./k8s/charts/frontend \
  --set image.repository=todo-frontend \
  --set image.tag=latest \
  --set service.type=NodePort \
  --set service.nodePort=30080
```

### Step 8: Verify Deployment

```bash
kubectl get pods
kubectl get services
```

**Expected Output**:
```
NAME                            READY   STATUS    RESTARTS   AGE
todo-backend-7d4f8b6c9-x2k4m   1/1     Running   0          2m
todo-backend-7d4f8b6c9-p9n3j   1/1     Running   0          2m
todo-frontend-5c8d9f7b2-k8m2   1/1     Running   0          1m
todo-frontend-5c8d9f7b2-m3n4   1/1     Running   0          1m

NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
todo-backend    ClusterIP  10.96.123.45     <none>        8000/TCP       2m
todo-frontend   NodePort   10.96.234.56     <none>        3000:30080/TCP 1m
```

### Step 9: Access the Application

```bash
minikube service todo-frontend --url
```

Or open in browser:
```
http://<minikube-ip>:30080
```

Get Minikube IP:
```bash
minikube ip
```

### Step 10: Test the Chatbot

Open the application and try:
```
"Add task buy milk tomorrow"
"Show my pending tasks"
"Complete task 1"
```

---

## Debugging

### Check Pod Status

```bash
kubectl get pods
kubectl describe pod <pod-name>
```

### View Logs

```bash
kubectl logs -f deployment/todo-backend
kubectl logs -f deployment/todo-frontend
```

### AI-Assisted Debugging with kubectl-ai

```bash
kubectl-ai "check why todo-backend pod is crashing"
kubectl-ai "show me the logs of todo-backend pod"
kubectl-ai "restart the todo-frontend deployment"
```

### Cluster Health with kagent

```bash
kagent "analyze the cluster health"
kagent "optimize resource allocation for todo apps"
```

---

## Common Issues

### Pods Not Starting

**Issue**: Pods stuck in `Pending` or `CrashLoopBackOff`

**Solution**:
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

Check if images are loaded:
```bash
minikube image list | grep todo
```

### Database Connection Failed

**Issue**: Backend can't connect to Neon PostgreSQL

**Solution**:
1. Verify DATABASE_URL secret:
   ```bash
   kubectl get secret todo-secrets -o jsonpath='{.data.DATABASE_URL}' | echo <base64-decoded-value>
   ```
2. Check network connectivity from pod

### Frontend Not Accessible

**Issue**: Can't access frontend via browser

**Solution**:
1. Verify service is NodePort:
   ```bash
   kubectl get service todo-frontend
   ```
2. Check Minikube tunnel:
   ```bash
   minikube service todo-frontend
   ```

---

## Cleanup

### Remove Helm Releases

```bash
helm uninstall todo-frontend
helm uninstall todo-backend
```

### Stop Minikube

```bash
minikube stop
```

### Delete Minikube Cluster

```bash
minikube delete
```

---

## Next Steps

1. **Optimization**: Use kagent to analyze and optimize resource allocation
2. **Scaling**: Adjust replicas and resource limits based on usage
3. **Monitoring**: Enable Prometheus/Grafana for advanced monitoring
4. **CI/CD**: Set up automated deployment pipeline

---

## AI Prompts Reference

### Gordon (Docker AI)
```
docker ai "generate production-ready multi-stage Dockerfile for FastAPI backend"
docker ai "create .dockerignore for Next.js frontend"
docker ai "optimize this Dockerfile for smaller image size"
```

### kubectl-ai
```
kubectl-ai "create Helm chart for backend service with 2 replicas"
kubectl-ai "deploy the todo frontend with NodePort on 30080"
kubectl-ai "check why pod is crashing and fix it"
kubectl-ai "setup horizontal pod autoscaler for backend"
```

### kagent
```
kagent "analyze the cluster health"
kagent "optimize resource allocation for todo apps"
kagent "suggest improvements for high availability"
```

---

**Estimated Time**: 30-45 minutes for first-time setup, 5-10 minutes for subsequent deployments
