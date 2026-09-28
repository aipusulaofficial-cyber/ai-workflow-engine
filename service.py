import time

from fastapi import FastAPI, HTTPException
from fastapi import Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel, Field

from observability import configure_observability, get_logger
from runtime_evidence import request_id_from_headers, runtime_evidence
from workflow_domain import Workflow


configure_observability()
logger = get_logger(__name__)
app = FastAPI(title="ai-workflow-engine", version="1.0.0")
tracer = trace.get_tracer("ai-workflow-engine")


class WorkflowPayload(BaseModel):
    steps: list[str] = Field(min_length=1, max_length=1_000)


class WorkflowRequest(BaseModel):
    key: str = Field(min_length=1, max_length=128, pattern=r".*\S.*")
    payload: WorkflowPayload


@app.middleware("http")
async def observability_headers(request: FastAPIRequest, call_next):
    started = time.perf_counter()
    request_id = request_id_from_headers(request.headers)
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-correlation-id"] = request.headers.get("x-correlation-id", request_id)
    response.headers["x-latency-ms"] = f"{(time.perf_counter() - started) * 1000:.3f}"
    return response


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/workflows")
def handle(request: WorkflowRequest, http_request: FastAPIRequest):
    started = time.perf_counter()
    request_id = request_id_from_headers(http_request.headers)
    with tracer.start_as_current_span("workflow.start") as span:
        span.set_attribute("workflow.key", request.key)
        try:
            workflow = Workflow(request.payload.steps)
            workflow.start()
            logger.info("workflow_started key=%s steps=%d", request.key, len(workflow.steps))
            return {
                "state": workflow.state,
                "steps": workflow.steps,
                "evidence": runtime_evidence(
                    request_id=request_id,
                    stage="workflow.start",
                    decision="ALLOW",
                    started=started,
                ),
            }
        except (ValueError, RuntimeError) as exc:
            evidence = runtime_evidence(
                request_id=request_id,
                stage="workflow.start",
                decision="FAIL",
                started=started,
                error=str(exc),
            )
            logger.warning(
                "workflow_rejected key=%s reason=%s", request.key, exc
            )
            raise HTTPException(
                status_code=400,
                detail={"error": str(exc), "evidence": evidence},
            ) from exc
