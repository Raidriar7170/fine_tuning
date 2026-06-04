## MODIFIED Requirements

### Requirement: Keep reports public-safe
The system SHALL prevent public reports, committed Human Brief HTML, and loop reports from leaking raw private rows, absolute local paths, private remote paths, secrets, tokens, or unreleased private details.

#### Scenario: Generate public report
- **WHEN** a report or committed Human Brief is written for public or reviewer-facing documentation
- **THEN** it contains aggregate metrics, sanitized examples, manifest references, and explicit claim boundaries without raw local/private corpus rows, local absolute paths, private remote paths, host details, or path-like private infrastructure examples
