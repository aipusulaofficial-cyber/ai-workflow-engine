from workflow_domain import State, Workflow


def test_workflow():
    w = Workflow(["a", "b"])
    w.start()
    w.complete_step("a")
    w.complete_step("b")
    assert w.state == State.SUCCEEDED
