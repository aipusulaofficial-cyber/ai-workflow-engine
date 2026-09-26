# AI Workflow Engine

A workflow execution engine for deterministic state transitions, controlled retries, failure isolation and observable job execution.

## Execution model
```text
workflow definition -> validation -> state transition -> task execution -> retry/failure policy -> terminal state + evidence
```

## Core contracts
- Workflow definitions are validated before execution.
- State transitions are explicit and testable.
- Retry behavior is bounded and policy-driven.
- Failures are isolated to the appropriate execution boundary.
- Execution context is available for operational diagnosis.

Orchestration policy is separated from infrastructure adapters so task implementations can change independently.

## Reliability
Timeouts, retries and failure states are part of the execution contract. A failed task cannot silently become a successful workflow outcome.

## Verification
CI covers contract and failure paths, with security and production validation as delivery gates.

## Evidence
[ARCHITECTURE.md](ARCHITECTURE.md) · [docs/PRINCIPAL-ENGINEERING.md](docs/PRINCIPAL-ENGINEERING.md) · [ADRs](ADRs/)

**Engineering chain:** Code → Contract → Test → Security → Runtime → Observability → Deployment → Evidence.