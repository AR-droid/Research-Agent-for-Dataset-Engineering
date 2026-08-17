# ARES --- Product Requirements Document

## 1. Product Overview

ARES is a full-stack platform for constructing structured,
evidence-grounded research datasets from scientific literature.

Researchers currently perform a largely manual workflow:

1.  search for sources
2.  collect papers
3.  download documents
4.  read them
5.  extract information
6.  enter results into spreadsheets
7.  verify values
8.  resolve duplicates
9.  reconcile conflicting results
10. track provenance
11. update datasets

ARES automates this workflow with bounded AI agents, deterministic
validation, persistent jobs, provenance, dataset versioning, and human
review.

## 2. Users

### Researcher

Creates projects, defines schemas, launches research runs, reviews
records, and publishes datasets.

### Reviewer

Reviews low-confidence records and conflicts.

### Administrator

Manages organization-level users, roles, settings, and access.

## 3. Core User Journey

### Create Project

A user creates:

-   project name
-   research question
-   description
-   inclusion criteria
-   exclusion criteria
-   date range
-   source configuration

### Define Dataset Schema

The user creates fields with:

-   name
-   display name
-   type
-   description
-   required/optional
-   evidence requirement
-   confidence threshold

### Run Research

The system:

1.  validates the research specification
2.  plans the workflow
3.  discovers candidate sources
4.  acquires permitted documents
5.  processes documents
6.  extracts structured fields
7.  validates evidence
8.  detects duplicates
9.  detects conflicts
10. creates review tasks
11. publishes approved records

## 4. Functional Requirements

### Authentication

-   registration/login
-   secure session handling
-   logout
-   password recovery or managed authentication
-   protected routes

### Organizations

Roles:

-   OWNER
-   ADMIN
-   RESEARCHER
-   REVIEWER
-   VIEWER

All data access must respect organization/project permissions.

### Projects

Users can:

-   create
-   edit
-   archive
-   view
-   configure
-   start runs

### Schema Builder

Initial field types:

-   text
-   number
-   integer
-   boolean
-   date
-   enum
-   list

Schema versions must be preserved.

### Source Discovery

ARES must support pluggable scholarly providers.

Initial candidates:

-   OpenAlex
-   Semantic Scholar
-   arXiv

The exact provider set is an implementation decision.

### Documents

Initial format: PDF.

Requirements:

-   file validation
-   size limits
-   secure storage
-   text extraction
-   page preservation
-   processing status
-   retries
-   failure handling

### Extraction

Extract according to the user-defined schema.

Each extracted field must contain:

-   value
-   confidence
-   provenance
-   validation status

Missing information must remain missing.

### Evidence

Users must be able to navigate:

``` text
Dataset
→ Record
→ Field
→ Evidence
→ Source
```

### Validation

Possible states:

-   VERIFIED
-   PROBABLE
-   UNCERTAIN
-   CONFLICTING
-   MISSING

### Deduplication

Identify:

-   exact duplicates
-   likely duplicates
-   versions of the same publication

Ambiguous cases go to review.

### Conflicts

Preserve conflicting values and their evidence.

The system may propose contextual reconciliation but must not silently
erase evidence.

### Human Review

Reviewers can:

-   approve
-   edit
-   reject
-   mark unresolved
-   resolve conflict

Decisions are auditable.

### Dataset Versioning

Published versions are immutable.

Users can compare:

-   records
-   fields
-   evidence
-   confidence
-   validation state

### Search

Support structured filtering and text search.

Semantic search may be added where useful.

### Export

Initial formats:

-   CSV
-   JSON

Exports correspond to a dataset version.

### Agent Runs

Users can inspect:

-   status
-   current stage
-   progress
-   errors
-   retries
-   review tasks
-   duration
-   model usage
-   cost when available

Private model chain-of-thought must never be displayed.

## 5. Non-Functional Requirements

### Reliability

-   asynchronous long-running work
-   retries
-   idempotency
-   resumability
-   explicit failure states

### Security

Protect against:

-   prompt injection
-   malicious documents
-   SSRF
-   path traversal
-   unauthorized access
-   cross-tenant leakage
-   secrets exposure

### Observability

-   structured logs
-   request IDs
-   job IDs
-   agent run IDs
-   metrics
-   traces
-   audit logs

### Scalability

The API and workers should be independently scalable.

### Maintainability

Business logic must not depend directly on a particular LLM or source
provider.

## 6. UI Requirements

ARES must be a research workspace, not a chatbot.

Primary areas:

-   Dashboard
-   Research Projects
-   Project Workspace
-   Dataset Builder
-   Dataset Explorer
-   Evidence
-   Review Queue
-   Conflicts
-   Agent Runs
-   Dataset Versions
-   Settings

Visual direction:

-   warm cream/off-white background
-   lime/acid-green accent
-   thin dark borders
-   modular cards
-   editorial layout
-   generous whitespace
-   monospace technical accents
-   clean sans-serif typography
-   minimal gradients
-   restrained shadows
-   subtle interactions

## 7. MVP

The first production slice must include:

-   authentication
-   project management
-   schema builder
-   source discovery
-   PDF ingestion
-   document processing
-   extraction
-   evidence
-   validation
-   human review
-   dataset publication
-   versioning
-   export
-   agent monitoring

Explicitly post-MVP:

-   autonomous experiments
-   automatic paper writing
-   broad web crawling
-   advanced research hypothesis generation
-   large-scale knowledge graphs
-   mobile application

## 8. Definition of Product Success

The deployed product must support the complete workflow from sign-up
through dataset export using real backend functionality, persistent
data, real jobs, real agent execution, and production error handling.
