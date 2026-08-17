# ARES --- Data Model

## 1. Goals

The data model must support:

-   multi-user access
-   organizations
-   research projects
-   custom schemas
-   versioned datasets
-   source provenance
-   document processing
-   evidence
-   agent runs
-   reviews
-   conflicts
-   exports
-   auditability

PostgreSQL is the authoritative system of record.

## 2. Core Relationships

``` text
Organization
 ├── Membership → User
 └── ResearchProject
       ├── Dataset
       │    ├── DatasetSchema
       │    └── DatasetVersion
       │          └── DatasetRecord
       │                └── DatasetFieldValue
       │                      └── Evidence
       │                            └── Document
       │                                  └── Source
       ├── AgentRun
       ├── ReviewTask
       └── Conflict
```

## 3. User

Purpose: authenticated application user.

Important fields:

-   id
-   email
-   display_name
-   password/auth-provider identifier
-   status
-   created_at
-   updated_at

Constraints:

-   unique email where applicable
-   secure credential handling

## 4. Organization

Purpose: tenant/workspace boundary.

Fields:

-   id
-   name
-   slug
-   created_at
-   updated_at

## 5. Membership

Fields:

-   id
-   organization_id
-   user_id
-   role
-   created_at
-   updated_at

Unique:

``` text
organization_id + user_id
```

Roles:

-   OWNER
-   ADMIN
-   RESEARCHER
-   REVIEWER
-   VIEWER

## 6. ResearchProject

Fields:

-   id
-   organization_id
-   name
-   description
-   research_question
-   inclusion_criteria
-   exclusion_criteria
-   date_from
-   date_to
-   status
-   created_by
-   created_at
-   updated_at
-   archived_at

## 7. Dataset

Represents the logical dataset belonging to a project.

Fields:

-   id
-   project_id
-   name
-   description
-   status
-   created_at
-   updated_at

## 8. DatasetSchema

Logical schema identity.

Fields:

-   id
-   dataset_id
-   name
-   description
-   current_version_id
-   created_at
-   updated_at

## 9. DatasetSchemaVersion

Immutable schema definition.

Fields:

-   id
-   schema_id
-   version_number
-   definition_json
-   created_by
-   created_at

Schema fields should contain:

-   key
-   label
-   type
-   description
-   required
-   evidence_required
-   confidence_threshold

## 10. DatasetVersion

Immutable published snapshot.

Fields:

-   id
-   dataset_id
-   version_number
-   schema_version_id
-   status
-   created_by
-   created_at
-   published_at

## 11. DatasetRecord

A logical research item in a dataset version.

Fields:

-   id
-   dataset_version_id
-   source_id
-   record_status
-   created_at
-   updated_at

A record may represent a paper or other research source.

## 12. DatasetFieldValue

Stores a value for a schema field.

Fields:

-   id
-   record_id
-   field_key
-   value_json
-   confidence
-   validation_status
-   source_evidence_id
-   created_at
-   updated_at

Unique:

``` text
record_id + field_key
```

## 13. Source

Represents scholarly source metadata.

Fields:

-   id
-   provider
-   external_id
-   doi
-   title
-   publication_year
-   venue
-   metadata_json
-   canonical_url
-   created_at
-   updated_at

Provider + external_id should be unique where possible.

## 14. Document

Represents an acquired research document.

Fields:

-   id
-   source_id
-   storage_key
-   content_type
-   file_size
-   checksum
-   processing_status
-   page_count
-   extracted_text_storage_key
-   error_code
-   created_at
-   updated_at

Checksum should support idempotent acquisition.

## 15. Evidence

First-class provenance object.

Fields:

-   id
-   document_id
-   page_number
-   section
-   table_reference
-   paragraph_reference
-   character_start
-   character_end
-   quoted_text_or_reference
-   extraction_context
-   created_at

Avoid storing unnecessarily large duplicate text if a stable document
reference is sufficient.

## 16. AgentRun

Represents a workflow execution.

Fields:

-   id
-   project_id
-   run_type
-   status
-   current_stage
-   input_snapshot
-   output_summary
-   retry_count
-   model_metadata
-   usage_metadata
-   cost_metadata
-   started_at
-   completed_at
-   error_details

## 17. AgentAction

Audit-friendly action record.

Fields:

-   id
-   agent_run_id
-   stage
-   action_type
-   tool_name
-   input_metadata
-   output_metadata
-   status
-   duration_ms
-   error_details
-   created_at

Do not store private chain-of-thought.

## 18. ReviewTask

Fields:

-   id
-   project_id
-   record_id
-   field_value_id
-   type
-   status
-   priority
-   assigned_to
-   reason
-   decision
-   decision_note
-   created_at
-   resolved_at

## 19. Conflict

Fields:

-   id
-   project_id
-   record_id
-   field_key
-   status
-   description
-   resolution
-   resolved_by
-   resolved_at
-   created_at

Conflicting evidence must remain accessible.

## 20. ExportJob

Fields:

-   id
-   dataset_version_id
-   format
-   status
-   storage_key
-   error_details
-   created_by
-   created_at
-   completed_at

## 21. AuditLog

Fields:

-   id
-   organization_id
-   actor_type
-   actor_id
-   action
-   resource_type
-   resource_id
-   metadata
-   created_at

Audit logs should be append-oriented.

## 22. Status Design

Prefer explicit state enums over ambiguous booleans.

Examples:

``` text
Document:
DISCOVERED
DOWNLOADING
PROCESSED
FAILED

Review:
PENDING
IN_PROGRESS
APPROVED
REJECTED
RESOLVED

AgentRun:
QUEUED
RUNNING
PAUSED
COMPLETED
FAILED
CANCELLED
```

## 23. Versioning Rule

Published dataset versions and schema versions are immutable.

Corrections create new versions or controlled revisions according to the
finalized product workflow.

## 24. Indexing

Likely indexes:

-   organization membership
-   project organization
-   source provider/external ID
-   source DOI
-   dataset/version
-   record/version
-   review status
-   agent run status
-   job status
-   created_at fields used for timelines

Indexes should be added based on actual query patterns rather than
speculatively.
