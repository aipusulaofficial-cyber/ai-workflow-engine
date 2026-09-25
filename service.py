from fastapi import FastAPI
from pydantic import BaseModel
from opentelemetry import trace
app=FastAPI(title="ai-workflow-engine",version="1.0.0");tracer=trace.get_tracer("ai-workflow-engine")
class Request(BaseModel):key:str;payload:dict={}
@app.get("/health/live")
def live():return {"status":"ok"}
@app.get("/health/ready")
def ready():return {"status":"ready"}
@app.post("/v1/workflow")
def handle(r:Request):
 with tracer.start_as_current_span("workflow"):return {"status":"accepted","key":r.key}
