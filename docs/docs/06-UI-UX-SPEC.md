# ARES --- UI/UX Specification

## 1. Product Experience

ARES must feel like a professional research instrument.

It should not feel like:

-   a chatbot
-   a generic SaaS dashboard
-   an AI landing page
-   an admin template

The user should feel that they are operating a research workspace.

## 2. Visual Reference

The supplied visual reference establishes the desired design language:

-   warm cream/off-white canvas
-   bright lime/acid-green accents
-   black/dark thin borders
-   modular cards
-   editorial composition
-   generous whitespace
-   technical typography
-   subtle playful details
-   minimal gradients
-   restrained shadows

Use these principles without copying the reference's branding, content,
or exact layout.

## 3. Typography

Use a clean sans-serif for normal interface text.

Use a monospace family for:

-   dataset values
-   IDs
-   timestamps
-   system statuses
-   agent events
-   technical metadata

Typography should create a strong distinction between research content
and system information.

## 4. Color Roles

Primary canvas:

-   warm off-white

Primary accent:

-   lime/acid green

Primary text:

-   near-black

Secondary text:

-   muted dark gray

State colors should be used sparingly and consistently.

Do not create a rainbow dashboard.

## 5. Layout

Use:

-   thin borders
-   modular panels
-   generous spacing
-   clear section headers
-   responsive grids
-   dense tables only where data exploration benefits from density

Avoid excessive cards nested inside cards.

## 6. Application Shell

Primary navigation:

-   Overview
-   Research Projects
-   Datasets
-   Review
-   Evidence
-   Agent Runs
-   Analytics
-   Settings

The exact navigation may change during implementation.

## 7. Dashboard

Show:

### Project Summary

-   active projects
-   running research runs
-   pending reviews

### Dataset Health

-   records
-   completeness
-   evidence coverage
-   conflicts
-   duplicates
-   low-confidence fields

### Agent Activity

Timeline of meaningful actions.

### Review Queue

Highest-priority unresolved tasks.

## 8. Project Workspace

A project should provide:

-   research objective
-   dataset status
-   source counts
-   record counts
-   evidence coverage
-   review state
-   recent agent activity

Suggested tabs:

-   Overview
-   Sources
-   Dataset
-   Evidence
-   Review
-   Conflicts
-   Runs
-   Versions

## 9. Schema Builder

Users should visually define fields.

Each field editor includes:

-   name
-   type
-   description
-   required
-   evidence required
-   confidence threshold

Support drag/reorder where appropriate.

## 10. Research Run

The run interface should clearly show:

``` text
Planning
  ✓
Discovery
  ✓
Acquisition
  ✓
Processing
  →
Extraction
  →
Validation
  ○
Review
  ○
Publication
  ○
```

Display:

-   progress
-   counts
-   failures
-   pending review
-   elapsed time

## 11. Agent Activity

Show structured events:

``` text
DISCOVERY
OpenAlex search
42 candidates found

FILTERING
18 candidates matched criteria

EXTRACTION
91 records generated

VALIDATION
8 records require review
```

Never show hidden chain-of-thought.

## 12. Dataset Explorer

Features:

-   table
-   search
-   filters
-   sort
-   pagination
-   field visibility
-   record detail

The table should feel like a research dataset tool rather than an admin
table.

## 13. Record Detail

Show:

-   source metadata
-   extracted fields
-   confidence
-   validation status
-   evidence
-   history
-   conflicts
-   review status

Each field should allow evidence inspection.

## 14. Evidence Viewer

Users should be able to:

-   view source metadata
-   open relevant document
-   see page/section/table reference
-   inspect supporting evidence

The interface should make provenance obvious.

## 15. Review Queue

Review cards should show:

-   what needs review
-   extracted value
-   confidence
-   evidence
-   source
-   reason for review

Actions:

-   approve
-   edit
-   reject
-   unresolved

## 16. Conflict Interface

Present competing values side-by-side.

Include:

-   value
-   source
-   evidence
-   context
-   agent proposal
-   reviewer decision

Never hide conflicting evidence.

## 17. Dataset Versions

Show a version timeline.

Version comparison should display:

-   added records
-   removed records
-   changed values
-   changed evidence
-   changed confidence

## 18. Responsive Design

The application must work on:

-   desktop
-   laptop
-   tablet

Mobile should support core viewing/review workflows but does not need to
reproduce every dense dataset operation.

## 19. Accessibility

Implement:

-   semantic HTML
-   keyboard navigation
-   visible focus states
-   sufficient contrast
-   accessible forms
-   ARIA where needed
-   reduced-motion consideration

## 20. Interaction Design

Use subtle transitions for:

-   state changes
-   panel opening
-   progress
-   review actions

Avoid excessive animation.

## 21. UI State Requirements

Every asynchronous view needs:

-   loading state
-   empty state
-   error state
-   success state
-   retry action where relevant

Do not leave blank screens during loading.

## 22. Design Principle

The UI should make the system's uncertainty and evidence visible.

Trust should come from:

**evidence + provenance + status + human control**

rather than from visual claims of AI intelligence.
