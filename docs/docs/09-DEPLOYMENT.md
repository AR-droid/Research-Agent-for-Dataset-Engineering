# ARES --- Deployment Specification

## 1. Goal

ARES must be deployable as a real production application.

Deployment is part of the product, not a final afterthought.

## 2. Runtime Components

The expected production topology is:

``` text
Internet
   ↓
Frontend
   ↓
API
   ├── PostgreSQL
   ├── Redis
   └── Object Storage
           ↑
         Workers
           ↑
      Agent Jobs
```

## 3. Environments

At minimum:

### Local

Docker Compose or equivalent.

### Staging

Production-like environment used for integration testing.

### Production

Real user environment.

Each environment must have separate configuration and secrets.

## 4. Containers

The application should be containerized.

Likely services:

-   web
-   api
-   worker

Database and Redis may be managed services in production.

## 5. Frontend Deployment

The frontend should be deployed to a production hosting platform/CDN
appropriate for the chosen framework.

Requirements:

-   HTTPS
-   environment-specific API URL
-   build validation
-   caching strategy
-   error reporting

## 6. Backend Deployment

The API must:

-   expose health endpoints
-   load configuration from environment
-   run database migrations through controlled deployment
-   support graceful shutdown
-   emit structured logs

## 7. Workers

Workers process:

-   source discovery
-   document acquisition
-   parsing
-   extraction
-   validation
-   deduplication
-   conflict analysis
-   exports

Workers must support:

-   retry
-   timeout
-   graceful shutdown
-   idempotency

Worker count should be independently scalable.

## 8. Database

PostgreSQL should be managed where practical.

Production requirements:

-   backups
-   migration process
-   connection limits
-   monitoring
-   restore procedure

## 9. Redis

Used for:

-   job queue
-   short-lived cache
-   coordination where appropriate

Do not treat Redis as the authoritative system of record.

## 10. Object Storage

Store:

-   original PDFs
-   extracted document artifacts
-   generated exports
-   other large artifacts

Use signed URLs where appropriate.

## 11. Secrets

Production secrets must use managed secret storage.

Never commit secrets.

Required categories may include:

-   database credentials
-   Redis credentials
-   LLM API keys
-   source-provider API keys
-   authentication secrets
-   object-storage credentials

## 12. CI/CD

GitHub Actions should run on pull requests and main branch changes.

CI should include:

-   backend tests
-   frontend tests
-   type checking
-   linting
-   build
-   migration validation
-   security/dependency checks where practical

## 13. Deployment Flow

Recommended:

``` text
Pull Request
 ↓
CI
 ↓
Review
 ↓
Merge
 ↓
Build
 ↓
Deploy Staging
 ↓
Smoke Tests
 ↓
Production Approval
 ↓
Deploy Production
```

## 14. Database Migrations

Migrations must be version controlled.

Deployment should never silently modify production schema outside the
migration system.

## 15. Health Checks

Provide:

``` text
/health
/ready
```

Health should verify process availability.

Readiness may verify critical dependencies according to the deployment
environment.

## 16. Observability

Production should collect:

-   application logs
-   worker logs
-   request metrics
-   job metrics
-   agent run metrics
-   error events
-   infrastructure metrics where available

## 17. Rollback

Every production deployment should have a rollback strategy.

Database migrations must be designed with compatibility and rollback
considerations.

## 18. Backup and Recovery

Define:

-   database backup schedule
-   retention
-   restore procedure
-   object storage durability/backup strategy

A backup is not considered reliable until restoration has been tested.

## 19. Cost Control

For an individual developer project:

-   use managed services where they reduce operational burden
-   avoid Kubernetes initially
-   scale workers independently
-   limit agent execution budgets
-   cache deterministic source metadata
-   avoid unnecessary model calls
-   monitor AI cost

## 20. Production Hardening

Before public release verify:

-   authentication
-   authorization
-   HTTPS
-   secrets
-   rate limits
-   input validation
-   file limits
-   SSRF protections
-   tenant isolation
-   logging
-   monitoring
-   backups
-   migrations
-   CI/CD
-   error handling

## 21. Deployment Principle

The production system should be simple enough for one developer to
operate but structured enough to evolve into a larger system.
