# ARES --- Testing & Evaluation

## 1. Goal

ARES must be evaluated as a software system and as an AI system.

A feature is not complete because an LLM returned a plausible answer.

## 2. Testing Layers

### Unit Tests

Test:

-   domain logic
-   validation
-   schema handling
-   state transitions
-   permissions
-   deterministic deduplication
-   utility functions

### Integration Tests

Test:

-   PostgreSQL
-   API/database integration
-   worker/database integration
-   source provider adapters
-   object storage
-   queue behavior

### API Tests

Test:

-   authentication
-   authorization
-   validation
-   pagination
-   filtering
-   error responses
-   idempotency

### End-to-End Tests

Critical path:

``` text
Register/Login
 ↓
Create Project
 ↓
Create Dataset Schema
 ↓
Start Research Run
 ↓
Discover Source
 ↓
Process Document
 ↓
Extract Record
 ↓
Validate Evidence
 ↓
Create Review Task
 ↓
Approve
 ↓
Publish Dataset
 ↓
Export Dataset
```

## 3. Gold-Standard Evaluation Corpus

Create:

``` text
evaluation/
├── documents/
└── ground_truth/
```

Use 10--20 initial research papers.

Include difficult examples:

-   tables
-   missing information
-   conflicting results
-   multiple versions
-   poor PDF formatting
-   supplementary material
-   ambiguous terminology

## 4. Ground Truth

Each document should define expected outputs for relevant fields.

Example:

``` json
{
  "paper_id": "paper-001",
  "fields": {
    "hardware": {
      "value": "STM32H743",
      "evidence_page": 7
    },
    "latency_ms": {
      "value": 12.4,
      "evidence_page": 8
    }
  }
}
```

The exact schema will depend on the selected benchmark.

## 5. Extraction Metrics

Measure:

### Precision

How many extracted values are correct?

### Recall

How many expected values were extracted?

### F1

Balance precision and recall.

## 6. Evidence Metrics

Measure:

-   evidence correctness
-   evidence coverage
-   page/section accuracy
-   unsupported claim rate

## 7. Provenance Metrics

Measure whether each persisted field can be traced to the correct
source.

## 8. Deduplication Metrics

Measure:

-   duplicate precision
-   duplicate recall
-   false merge rate

False merges are especially important because incorrectly merging
research records can corrupt a dataset.

## 9. Conflict Metrics

Measure:

-   conflict detection recall
-   false conflict rate
-   resolution quality

## 10. Confidence Calibration

Compare predicted confidence to actual correctness.

A high-confidence incorrect extraction should be treated as a serious
failure.

## 11. Reliability Metrics

Track:

-   job success rate
-   retry rate
-   failed workflow rate
-   mean processing time
-   provider error rate

## 12. Cost Metrics

Track:

-   tokens per document
-   model calls per document
-   cost per document
-   cost per accepted record

## 13. Regression Evaluation

Every major agent change should be evaluated against the fixed corpus.

Do not allow an optimization that improves one example while silently
degrading the overall benchmark.

## 14. Human Review Metrics

Track:

-   review rate
-   reviewer correction rate
-   average review time
-   disagreement rate
-   percentage of records accepted without changes

## 15. Evaluation Philosophy

The primary optimization target is:

> **High-quality evidence-grounded records with low unsupported-claim
> rates.**

Not:

> Maximum number of records generated.

## 16. Test Environments

Maintain:

-   local
-   CI
-   staging
-   production

Production data should never be used as an uncontrolled test
environment.

## 17. Definition of Done

A major feature requires:

-   unit tests
-   integration tests where applicable
-   E2E coverage where applicable
-   agent evaluation where applicable
-   documentation
-   failure handling
-   observability
