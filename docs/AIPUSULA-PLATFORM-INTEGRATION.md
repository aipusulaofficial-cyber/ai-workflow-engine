# AIPusula Platform Integration — Governed Workflows

Workflow execution follows request -> policy -> task graph -> governed tool/model calls -> state -> evaluation -> audit.

Enforce time, retry, token and cost budgets per workflow. Persist state through an abstraction that supports idempotency and recovery.

Engineering standard: Code -> Contract -> Test -> Security -> Runtime -> Observability -> Deployment -> Evidence
