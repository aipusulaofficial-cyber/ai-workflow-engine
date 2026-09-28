from runtime_evidence import runtime_evidence
import time

def test_foundation_contract():
    e=runtime_evidence(request_id="foundation",stage="workflow",decision="ALLOW",started=time.perf_counter())
    assert e["stage"] == "workflow"
    assert e["decision"] == "ALLOW"
