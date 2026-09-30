import pytest

from workflow_engine import Task, Workflow, WorkflowError


def test_second_run_terminates_without_reexecuting_completed_tasks():
    invoked = []
    workflow = Workflow([Task("a"), Task("b", ("a",))])
    handlers = {
        "a": lambda: invoked.append("a"),
        "b": lambda: invoked.append("b"),
    }
    assert workflow.run(handlers) == ["a", "b"]
    assert workflow.run(handlers) == ["a", "b"]
    assert invoked == ["a", "b"]


@pytest.mark.parametrize("retries", [-1, 1.5, True])
def test_invalid_retry_counts_rejected(retries):
    workflow = Workflow([Task("a")])
    with pytest.raises(ValueError, match="retries"):
        workflow.run({"a": lambda: None}, retries=retries)


def test_duplicate_task_names_rejected():
    with pytest.raises(WorkflowError, match="duplicate"):
        Workflow([Task("duplicate"), Task("duplicate")])
