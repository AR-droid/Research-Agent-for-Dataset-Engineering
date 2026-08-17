# ARES --- API Specification

## 1. API Principles

The API exposes domain operations rather than raw database operations.

Requirements:

-   typed request/response models
-   authentication
-   authorization
-   validation
-   consistent errors
-   pagination
-   filtering
-   idempotency where appropriate
-   request correlation IDs

## 2. Authentication

Illustrative endpoints:

``` text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

Exact authentication mechanism is an architecture decision.

## 3. Organizations

``` text
GET  /api/v1/organizations
GET  /api/v1/organizations/{organization_id}
GET  /api/v1/organizations/{organization_id}/members
POST /api/v1/organizations/{organization_id}/members
PATCH /api/v1/organizations/{organization_id}/members/{member_id}
```

## 4. Projects

``` text
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}
```

Project creation should accept:

-   name
-   description
-   research question
-   criteria
-   date range

## 5. Dataset

``` text
GET  /api/v1/projects/{project_id}/datasets
POST /api/v1/projects/{project_id}/datasets
GET  /api/v1/datasets/{dataset_id}
PATCH /api/v1/datasets/{dataset_id}
```

## 6. Schema

``` text
GET  /api/v1/datasets/{dataset_id}/schema
POST /api/v1/datasets/{dataset_id}/schema/versions
GET  /api/v1/datasets/{dataset_id}/schema/versions
GET  /api/v1/datasets/{dataset_id}/schema/versions/{version_id}
```

Schema creation must validate field keys and types.

## 7. Research Runs

``` text
POST /api/v1/projects/{project_id}/runs
GET  /api/v1/runs/{run_id}
POST /api/v1/runs/{run_id}/pause
POST /api/v1/runs/{run_id}/resume
POST /api/v1/runs/{run_id}/cancel
```

Run creation should be idempotent where appropriate.

## 8. Sources

``` text
GET  /api/v1/projects/{project_id}/sources
GET  /api/v1/sources/{source_id}
POST /api/v1/projects/{project_id}/sources/search
```

Source provider access should be hidden behind service interfaces.

## 9. Documents

``` text
POST /api/v1/sources/{source_id}/documents
GET  /api/v1/documents/{document_id}
GET  /api/v1/documents/{document_id}/status
```

Large file uploads should use signed object-storage URLs where
appropriate.

## 10. Records

``` text
GET /api/v1/datasets/{dataset_id}/records
GET /api/v1/records/{record_id}
GET /api/v1/records/{record_id}/evidence
```

Filtering should support schema-defined fields.

## 11. Reviews

``` text
GET  /api/v1/projects/{project_id}/reviews
GET  /api/v1/reviews/{review_id}
POST /api/v1/reviews/{review_id}/decision
```

Decision payload:

``` json
{
  "decision": "APPROVE",
  "edited_value": null,
  "note": "Evidence clearly supports the extracted value."
}
```

## 12. Conflicts

``` text
GET  /api/v1/projects/{project_id}/conflicts
GET  /api/v1/conflicts/{conflict_id}
POST /api/v1/conflicts/{conflict_id}/resolve
```

## 13. Dataset Versions

``` text
GET  /api/v1/datasets/{dataset_id}/versions
GET  /api/v1/datasets/{dataset_id}/versions/{version_id}
POST /api/v1/datasets/{dataset_id}/versions
GET  /api/v1/datasets/{dataset_id}/versions/compare
```

## 14. Exports

``` text
POST /api/v1/dataset-versions/{version_id}/exports
GET  /api/v1/exports/{export_id}
```

Large exports should be asynchronous.

## 15. Agent Runs

``` text
GET /api/v1/projects/{project_id}/agent-runs
GET /api/v1/agent-runs/{run_id}
GET /api/v1/agent-runs/{run_id}/actions
```

## 16. Health

``` text
GET /health
GET /ready
```

Health endpoints should not leak secrets or sensitive internals.

## 17. Errors

Use a consistent shape:

``` json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource does not exist.",
    "request_id": "..."
  }
}
```

Avoid returning internal exception details in production.

## 18. Pagination

Use a consistent pagination strategy across collection endpoints.

The exact cursor/offset mechanism is an implementation decision.

## 19. Authorization

Every resource lookup must enforce organization/project ownership.

Never rely only on frontend route protection.

## 20. API Versioning

Use a versioned prefix such as:

``` text
/api/v1
```

Breaking changes require a new API version or migration strategy.
