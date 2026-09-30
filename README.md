# AI Workflow Engine

[![CI](https://github.com/aipusulaofficial-cyber/ai-workflow-engine/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/ai-workflow-engine/actions/workflows/ci.yml)
[![Production Tests](https://github.com/aipusulaofficial-cyber/ai-workflow-engine/actions/workflows/production-tests.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/ai-workflow-engine/actions/workflows/production-tests.yml)
[![Security / SBOM](https://github.com/aipusulaofficial-cyber/ai-workflow-engine/actions/workflows/security-sbom.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/ai-workflow-engine/actions/workflows/security-sbom.yml)


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

## Portfolio evidence
[Portfolio evidence map](docs/PORTFOLIO_EVIDENCE.md) — executable proof, architecture mapping and reviewable CI evidence.
