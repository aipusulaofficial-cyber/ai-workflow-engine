from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from observability import configure_observability, get_logger
from workflow_domain import Workflow

configure_observability()
logger = get_logger(__name__)

app = FastAPI(title="ai-workflow-engine", version="1.0.0")
tracer = trace.get_tracer("ai-workflow-engine")


class WorkflowRequest(BaseModel):
    key: str
    payload: dict = {}


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/workflows")
def handle(request: WorkflowRequest):
    with tracer.start_as_current_span("workflow.start") as span:
        span.set_attribute("workflow.key", request.key)
        try:
            workflow = Workflow(list(request.payload.get("steps", [])))
            workflow.start()
            logger.info(
                "workflow_started key=%s steps=%d", request.key, len(workflow.steps)
            )
            return {"state": workflow.state, "steps": workflow.steps}
        except (ValueError, KeyError, RuntimeError) as exc:
            logger.warning("workflow_rejected key=%s reason=%s", request.key, exc)
            raise HTTPException(status_code=400, detail=str(exc)) from exc
