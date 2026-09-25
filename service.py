from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from workflow_domain import *
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"ai-workflow-engine"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="ai-workflow-engine",version="1.0.0");tracer=trace.get_tracer("ai-workflow-engine")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/workflows")
def handle(r:Request):
 with tracer.start_as_current_span("ai-workflow-engine.domain"):
  try: w=Workflow(list(r.payload.get("steps",[])));w.start();return {"state":w.state,"steps":w.steps}
  except (ValueError,KeyError,RuntimeError) as e: raise HTTPException(status_code=400,detail=str(e)) from e
