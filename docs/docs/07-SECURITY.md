# ARES --- Security Specification

## 1. Security Goal

ARES handles research documents, user data, source metadata, AI model
interactions, and potentially sensitive research workflows.

Security must be designed from the beginning.

## 2. Threat Model

Primary threats:

-   prompt injection in research documents
-   malicious PDFs
-   malicious external content
-   SSRF
-   path traversal
-   unauthorized access
-   cross-tenant data leakage
-   credential theft
-   API abuse
-   model/tool abuse
-   oversized files
-   denial-of-service
-   data corruption

## 3. Trust Boundaries

Treat as untrusted:

-   uploaded files
-   paper text
-   web content
-   extracted metadata
-   model-generated output
-   external API responses

Trusted:

-   validated application configuration
-   authenticated identity
-   server-side authorization logic
-   validated domain operations

## 4. Prompt Injection

External content must never be treated as instructions.

The model context should distinguish:

``` text
SYSTEM
APPLICATION
USER
EXTERNAL DOCUMENT
```

Document text must be explicitly labeled as untrusted data.

## 5. File Security

PDF ingestion must:

-   validate MIME/type
-   enforce size limits
-   generate safe storage keys
-   avoid trusting filenames
-   prevent path traversal
-   isolate processing
-   reject unsupported formats
-   record checksum

Do not execute document content.

## 6. SSRF

External URL fetching must:

-   use an allowlisted provider strategy where practical
-   reject localhost/private network targets
-   validate redirects
-   enforce timeouts
-   limit response size

## 7. Authentication

Passwords must never be stored in plaintext.

Use established authentication libraries/providers.

Sessions/tokens must have:

-   expiry
-   secure storage
-   revocation strategy where needed

## 8. Authorization

Enforce authorization server-side.

Every project/dataset/source/document request must verify organization
and project access.

Frontend hiding is not security.

## 9. Multi-Tenancy

Tenant identifiers must be part of authorization checks.

Queries should never assume a user can access a resource solely because
they know its ID.

## 10. Secrets

Never commit:

-   API keys
-   database passwords
-   tokens
-   private keys
-   credentials

Use environment variables locally and managed secret storage in
production.

## 11. Agent Tool Security

Agents must have explicit tool permissions.

Never give agents unrestricted:

-   shell
-   filesystem
-   database
-   network

access.

## 12. Rate Limiting

Rate-limit:

-   authentication
-   source discovery
-   document ingestion
-   expensive agent operations
-   exports

## 13. Data Protection

Use HTTPS in production.

Encrypt storage where supported.

Do not log:

-   credentials
-   tokens
-   full document contents
-   sensitive user data

## 14. Audit

Record important events:

-   authentication events
-   permission changes
-   dataset publication
-   reviewer decisions
-   schema changes
-   agent-triggered mutations
-   exports

## 15. Dependency Security

CI should include dependency/security checks where practical.

Pin or constrain dependencies appropriately.

## 16. Database Security

Use:

-   least-privilege database users
-   parameterized queries
-   migrations
-   backups
-   connection encryption in production where supported

## 17. AI Security

Validate model outputs before persistence.

Use:

-   structured outputs
-   schema validation
-   bounded retries
-   tool permissions
-   token/cost limits

## 18. Incident Response

Production should provide enough information to answer:

-   what happened?
-   which user/project was affected?
-   which job/agent run caused it?
-   what data changed?
-   when did it happen?
-   can the change be rolled back?

## 19. Security Principle

External research content is data, never authority.

No paper, web page, model response, or external source can override
application security policy.
