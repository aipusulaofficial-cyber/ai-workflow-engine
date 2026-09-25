import pytest

from workflow_engine import Task, Workflow, WorkflowError


def test_dag_order_and_retry():
    out = []
    calls = {"b": 0}

    def b():
        calls["b"] += 1
        if calls["b"] < 2:
            raise RuntimeError()
        out.append("b")

    w = Workflow([Task("a"), Task("b", ("a",))])
    w.run({"a": lambda: out.append("a"), "b": b})
    assert out == ["a", "b"]


def test_cycle_fails():
    with pytest.raises(WorkflowError):
        Workflow([Task("a", ("b",)), Task("b", ("a",))]).run({})


def test_missing_dependency():
    with pytest.raises(WorkflowError):
        Workflow([Task("a", ("x",))]).validate()
