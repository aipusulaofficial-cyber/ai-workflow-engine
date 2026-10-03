import pytest

from durable_workflow import DurableWorkflowStore


def test_invalid_transition_rejected(tmp_path):
    store = DurableWorkflowStore(tmp_path / "workflow.db")
    store.save("wf", "pending", "{}")
    with pytest.raises(ValueError):
        store.save("wf", "succeeded", "{}")
    assert store.load("wf")[1] == "pending"


def test_terminal_state_cannot_reopen(tmp_path):
    store = DurableWorkflowStore(tmp_path / "workflow.db")
    store.save("wf", "pending", "{}")
    store.save("wf", "running", "{}")
    store.save("wf", "succeeded", "{}")
    with pytest.raises(ValueError):
        store.save("wf", "running", "{}")


def test_terminal_workflow_payload_is_immutable(tmp_path):
    store = DurableWorkflowStore(tmp_path / "workflow.db")
    store.save("wf", "pending", "start")
    store.save("wf", "running", "running")
    store.save("wf", "succeeded", "original-evidence")
    with pytest.raises(ValueError, match="terminal workflow"):
        store.save("wf", "succeeded", "tampered-evidence")
    assert store.load("wf") == ("wf", "succeeded", "original-evidence")
