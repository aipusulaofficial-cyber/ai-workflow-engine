# ADR-0002: Production hardening
FastAPI exposes workflow control contracts and OpenTelemetry traces execution. Kubernetes/Helm define bounded runtime deployment; Terraform owns infrastructure inputs. Trivy/CycloneDX gate security/SBOM; contract/property tests protect inputs; Locust exercises load.
Retries and durable workflow state remain domain responsibilities; production externalizes persistence, secrets and telemetry.
