import time
import uuid

from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel, Field

from observability import configure_observability, get_logger
from workflow_domain import Workflow

configure_observability()
logger = get_logger(__name__)

app = FastAPI(title="ai-workflow-engine", version="1.0.0")
app.add_middleware(ObservabilityHeadersMiddleware)  # type: ignore[name-defined]
tracer = trace.get_tracer("ai-workflow-engine")


class Request(BaseModel):
    key: str
    payload: dict = Field(default_factory=dict)


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/workflows")
def handle(request: Request):
    with tracer.start_as_current_span("ai-workflow-engine.domain"):
        try:
            workflow = Workflow.create(request.key, request.payload)
            return {"workflow_id": workflow.workflow_id, "status": "accepted"}
        except (ValueError, KeyError, TypeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
