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
