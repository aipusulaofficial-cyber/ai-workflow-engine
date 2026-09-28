import time

from runtime_evidence import runtime_evidence


def test_foundation_contract():
    evidence = runtime_evidence(
        request_id="foundation", stage="workflow", decision="ALLOW", started=time.perf_counter()
    )
    assert evidence["stage"] == "workflow"
    assert evidence["decision"] == "ALLOW"
