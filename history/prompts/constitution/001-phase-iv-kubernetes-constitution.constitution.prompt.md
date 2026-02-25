---
id: 001
title: phase-iv-kubernetes-constitution
stage: constitution
date: 2026-02-23
surface: agent
model: qwen-code
feature: phase-iv-k8s-deployment
branch: phase-iv-kubernetes
user: AK C0M
command: /sp.constitution
labels: ["constitution", "phase-iv", "kubernetes", "deployment", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (Constitution document update)
---

## Prompt

/sp.constitution
Phase IV Constitution: Local Kubernetes Deployment of Todo AI Chatbot
Version: 1.0 | February 2026 | For Qwen + Spec-Kit Plus + Agentic Dev Stack

## 1. PROJECT OVERVIEW & INTEGRATION
Yeh Phase IV hai hackathon-todo project ka.  
Hum Phase III ke fully working AI Todo Chatbot (Next.js frontend + FastAPI backend + Better Auth + Neon Postgres + MCP tools + ChatKit) ko **local Kubernetes cluster** pe deploy kar rahe hain.

Goal: Zero-cost, production-like local deployment using modern Cloud-Native tools with heavy AI assistance.

**Previous Phases Integration**
- Phase I → Console Todo
- Phase II → Full-Stack Web (FastAPI + Next.js)
- Phase III → AI Chatbot with MCP tools
- **Phase IV → Kubernetes Deployment (Minikube + Helm + AI Agents)**

Sab kuch **same monorepo** (hackathon-todo/) mein rahega. Koi alag repo nahi.

## 2. CORE OBJECTIVE
Containerize frontend aur backend, Helm Charts banao, Minikube pe deploy karo, aur **kubectl-ai + kagent + Gordon** (Docker AI Agent) ka heavy use karke AI-assisted deployment karo.

## 3. NON-NEGOTIABLE RULES (Constitution)
- Har cheez Spec-Driven rahegi (@specs/ folder use karo)
- Gordon (Docker AI) ko maximum use karo containerization ke liye (agar unavailable ho to standard Docker CLI)
- kubectl-ai aur kagent ko real commands generate karne ke liye use karo (na ke manually likho)
- Helm Charts must be used (frontend aur backend ke alag charts + umbrella chart optional)
- Deployment fully local Minikube pe hona chahiye
- All previous Phase III functionality (chat, MCP tools, auth, DB) working rahe
- User isolation, JWT, Neon connection sab Kubernetes mein environment variables se configure ho
- No manual YAML writing without AI assistance (Gordon/kubectl-ai/kagent se generate karwao)

## 4. TECHNOLOGY STACK (Phase IV Specific)
- Containerization: Docker Desktop + **Gordon (Docker AI Agent)**
- Orchestration: Kubernetes (Minikube)
- Package Manager: Helm Charts
- AI DevOps Assistants: **kubectl-ai**, **kagent**
- Base Apps: Phase III (Next.js frontend + FastAPI backend)
- Database: Neon PostgreSQL (external, connection string env se)
- Monitoring/Debug: Minikube dashboard + kubectl-ai/kagent

## 5. AI TOOLS USAGE GUIDELINES
**Gordon (Docker AI Agent)**
- Pehle enable karo: Docker Desktop → Settings → Beta Features → Gordon on
- Use commands jaise:
  - `docker ai "containerize this Next.js frontend for production"`
  - `docker ai "generate multi-stage Dockerfile for FastAPI backend"`
  - `docker ai "create docker-compose.yml for local testing"`

**kubectl-ai**
- Use for all Kubernetes operations:
  - `kubectl-ai "deploy the todo frontend with 2 replicas and expose on port 3000"`
  - `kubectl-ai "create Helm chart for backend service"`
  - `kubectl-ai "check why pod is crashing and fix it"`

**kagent**
- Advanced analysis aur optimization ke liye:
  - `kagent "analyze the cluster health"`
  - `kagent "optimize resource allocation for todo apps"`
  - `kagent "suggest improvements for high availability"`

## 6. FOLDER STRUCTURE (New additions for Phase IV)

## Response snapshot

Updated the project constitution from Phase III (AI Chatbot with Cohere) to Phase IV (Kubernetes Deployment). The new constitution includes:

**Version**: 3.0.0 (MAJOR bump from 2.0.0)

**Key Changes**:
- Shifted focus from chatbot implementation to K8s deployment
- Added AI DevOps tools: Gordon, kubectl-ai, kagent
- Defined containerization standards with multi-stage Dockerfiles
- Mandated Helm Charts for frontend and backend
- Established local Minikube deployment guidelines
- Preserved Phase III functionality requirements
- Added K8s resource guidelines (limits, probes, services)
- Defined environment configuration via Secrets/ConfigMaps
- Added folder structure for docker/, helm/, k8s/ directories

**Removed**: Chatbot-specific sections (TodoMaster personality, chat flow, example behaviors) as they're implementation details, not deployment concerns.

## Outcome

- ✅ Impact: Constitution updated to Phase IV with complete Kubernetes deployment governance, AI tool guidelines, and deployment principles
- 🧪 Tests: N/A (document update, no code changes)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Consider running /sp.specify for Phase IV deployment spec, /sp.plan for deployment architecture, /sp.tasks for implementation tasks
- 🧠 Reflection: Phase IV constitution successfully transitions from application-level concerns to infrastructure/deployment-level governance while preserving all Phase III functionality requirements

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update completed successfully
- Graders run and results (PASS/FAIL): N/A (no grader for constitution documents)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create Phase IV deployment specification using /sp.specify command with focus on Minikube + Helm + AI tools
