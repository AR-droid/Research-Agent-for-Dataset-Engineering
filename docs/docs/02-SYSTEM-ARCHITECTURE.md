# ARES --- System Architecture

## 1. Goal

ARES must be a production-grade full-stack system that can run locally
and in a real cloud environment.

The initial architecture should be modular rather than prematurely
distributed.

## 2. Logical Architecture

``` text
Browser
   ↓
Frontend
   ↓
API
   ↓
Application Services
   ├── PostgreSQL
   ├── Redis / Job Queue
   └── Object Storage
             ↓
          Workers
             ↓
      Agent Orchestrator
       ├── Discovery
       ├── Extraction
       ├── Validation
       ├── Deduplication
       └── Conflict Analysis
             ↓
       External Providers
```

## 3. Technology Direction

Expected initial stack:

### Frontend

React + TypeScript.

### Backend

Python + FastAPI.

### Database

PostgreSQL.

### Queue/Cache

Redis.

### Workers

Python worker processes.

### Storage

S3-compatible object storage.

### Containers

Docker.

### CI/CD

GitHub Actions.

### AI

Provider-independent LLM abstraction.

Exact technologies should be finalized during architecture review.

## 4. Repository

Conceptual structure:

``` text
ares/
├── apps/
│   ├── web/
│   └── api/
├── workers/
├── packages/
│   └── shared/
├── infrastructure/
├── docs/
├── evaluation/
├── tests/
├── scripts/
├── .github/
├── README.md
├── .gitignore
└── docker-compose.yml
```

## 5. Backend Boundaries

``` text
API
 ↓
Application Services
 ↓
Domain Logic
 ↓
Repositories
 ↓
Database
```

External systems use adapters:

``` text
SourceProvider
LLMProvider
DocumentStorage
Queue
```

## 6. Core Entities

Initial entities:

-   User
-   Organization
-   Membership
-   ResearchProject
-   Dataset
-   DatasetSchema
-   DatasetSchemaVersion
-   DatasetVersion
-   DatasetRecord
-   DatasetFieldValue
-   Source
-   Document
-   Evidence
-   AgentRun
-   AgentAction
-   ReviewTask
-   Conflict
-   ExportJob
-   AuditLog

Add entities only when justified.

## 7. Agent Workflow

``` text
PLANNING
  ↓
DISCOVERING
  ↓
ACQUIRING
  ↓
PROCESSING
  ↓
EXTRACTING
  ↓
VALIDATING
  ↓
DEDUPLICATING
  ↓
CONFLICT_RESOLUTION
  ↓
REVIEW
  ↓
PUBLISHING
  ↓
COMPLETED
```

Failure states:

-   FAILED
-   PAUSED
-   CANCELLED

## 8. Evidence Model

Conceptually:

``` text
DatasetVersion
    ↓
DatasetRecord
    ↓
DatasetFieldValue
    ↓
Evidence
    ↓
Document
    ↓
Source
```

Evidence should reference stable document locations when possible:

-   page
-   section
-   table
-   paragraph
-   character offsets

## 9. Background Work

Asynchronous jobs:

-   source discovery
-   document acquisition
-   parsing
-   extraction
-   validation
-   deduplication
-   conflict analysis
-   exports

Jobs must support:

-   status
-   retries
-   timeout
-   cancellation
-   idempotency
-   progress
-   failure details

## 10. Security Architecture

External content is untrusted.

Separate:

-   system instructions
-   application instructions
-   user requirements
-   external document content

Never treat document text as trusted instructions.

Agents receive only scoped tools.

## 11. Observability

Trace:

``` text
HTTP Request
 → Application Service
 → Job
 → Agent Run
 → Tool Call
 → Database Mutation
```

Use request IDs, job IDs, and agent run IDs.

## 12. API Principles

APIs expose domain operations, not raw database operations.

Requirements:

-   typed request/response schemas
-   validation
-   authentication
-   authorization
-   pagination
-   filtering
-   consistent errors
-   idempotency where needed

## 13. Frontend Architecture

Use:

-   reusable components
-   typed API client
-   shared design tokens
-   loading/error/empty states
-   accessible forms
-   responsive layouts

Core surfaces:

-   dashboard
-   projects
-   schema builder
-   dataset explorer
-   evidence
-   review
-   conflicts
-   agent runs
-   versions
-   settings

## 14. Deployment

The production system should include:

-   frontend
-   API
-   workers
-   PostgreSQL
-   Redis
-   object storage
-   secrets management
-   health checks
-   migrations
-   backups
-   CI/CD
-   monitoring

The first deployment should be cost-conscious and avoid Kubernetes
unless justified.

## 15. Architectural Rule

Develop in vertical slices:

``` text
Frontend
 → API
 → Domain
 → Database
 → Worker/Agent
 → Result
 → Frontend
```

Do not build isolated layers and integrate only at the end.
