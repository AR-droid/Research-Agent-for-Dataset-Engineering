# ARES --- Agent Architecture

## 1. Purpose

The agentic layer automates research dataset construction while
preserving evidence, provenance, uncertainty, and human oversight.

ARES is not a general autonomous chatbot.

## 2. Operating Loop

``` text
Observe
 ↓
Understand State
 ↓
Select Authorized Action
 ↓
Call Tool
 ↓
Validate Result
 ↓
Persist Observation
 ↓
Update Workflow State
 ↓
Continue / Review / Complete
```

## 3. Orchestrator

The orchestrator controls:

-   workflow state
-   tasks
-   dependencies
-   retries
-   timeouts
-   agent invocation
-   termination
-   review transitions

The LLM must not be trusted to determine whether an application state
transition is valid.

## 4. Research Planner

Inputs:

-   research question
-   inclusion criteria
-   exclusion criteria
-   date range
-   dataset schema
-   source configuration

Output:

-   search strategy
-   source providers
-   document types
-   extraction requirements
-   validation requirements
-   review thresholds

## 5. Discovery Agent

Responsibilities:

-   search configured scholarly sources
-   rank candidate sources
-   record search provenance
-   avoid redundant searches
-   stop according to explicit discovery criteria

Possible tools:

-   search_sources
-   get_source_metadata
-   search_citations

The agent must never fabricate a source.

## 6. Acquisition

Primarily deterministic.

Responsibilities:

-   retrieve permitted documents
-   validate file type
-   enforce size limits
-   store documents
-   associate documents with sources
-   avoid duplicate downloads

## 7. Extraction Agent

Inputs:

-   processed document
-   dataset schema
-   research specification

Outputs:

-   structured field candidates
-   confidence
-   evidence reference
-   validation status

Missing data must remain missing.

## 8. Validation Agent

Checks whether extracted values are actually supported.

States:

-   VERIFIED
-   PROBABLE
-   UNCERTAIN
-   CONFLICTING
-   MISSING

Deterministic validation should be preferred when possible.

## 9. Deduplication

First use deterministic signals:

-   DOI
-   external source ID
-   normalized title
-   author/year combination

Use semantic similarity only for ambiguous cases.

## 10. Conflict Resolution

When values disagree:

1.  identify conflict
2.  retrieve evidence
3.  compare context
4.  determine comparability
5.  preserve all evidence
6.  propose resolution
7.  assign confidence
8.  request human review if needed

## 11. Human Review

Review is triggered by:

-   low confidence
-   conflicting evidence
-   ambiguous duplicates
-   unsupported extraction
-   schema ambiguity

Human decisions are authoritative and auditable.

## 12. Tool Permissions

Discovery:

-   source search
-   metadata retrieval

Extraction:

-   document reading
-   page/section retrieval

Validation:

-   evidence retrieval
-   document reading

No agent receives unrestricted shell or database access.

## 13. Structured Outputs

Pipeline:

``` text
LLM Output
 ↓
Schema Validation
 ↓
Business Validation
 ↓
Evidence Validation
 ↓
Persistence
```

Invalid outputs are retried within bounded limits.

Repeated failures become failed/review states.

## 14. Memory

Use explicit memory categories:

### Workflow Memory

Current run state.

### Source Memory

Processed/discovered sources.

### Research Memory

Validated project knowledge.

### Decision Memory

Important resolution decisions.

### Error Memory

Previous processing failures.

Do not automatically vectorize everything.

## 15. Budgets

Every run should support:

-   maximum iterations
-   maximum tool calls
-   execution timeout
-   token budget where measurable
-   cost budget where measurable

Budget exhaustion leads to PAUSED or REVIEW_REQUIRED.

## 16. Failure Classes

### Retryable

-   network timeout
-   provider outage
-   rate limit
-   temporary worker failure

### Non-retryable

-   invalid document
-   unsupported schema
-   authorization failure
-   malformed source

### Agent failure

-   repeated invalid outputs
-   tool misuse
-   budget exceeded
-   unresolved state

## 17. Observability

Show users actions and outcomes, not hidden chain-of-thought.

Example:

``` text
12:03
DISCOVERY
Search OpenAlex
42 candidates found

12:08
FILTERING
18 sources selected

12:14
EXTRACTION
91 records generated

12:17
VALIDATION
8 records require review
```

## 18. Evaluation

Maintain a gold-standard evaluation corpus.

Measure:

-   field precision
-   field recall
-   F1
-   evidence correctness
-   provenance accuracy
-   duplicate detection
-   conflict detection
-   review rate
-   cost/document
-   latency/document

## 19. Safety Principle

> Prefer an explicit uncertain state over an unsupported confident
> answer.

The system should optimize for trustworthy dataset construction, not
maximum autonomous completion.
