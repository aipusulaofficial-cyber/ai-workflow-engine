"""Workflow engine with DAG validation, retries and idempotent task execution."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    name: str
    deps: tuple[str, ...] = ()


class WorkflowError(Exception):
    pass


class Workflow:
    def __init__(self, tasks):
        task_list = list(tasks)
        if len({task.name for task in task_list}) != len(task_list):
            raise WorkflowError("duplicate task name")
        self.tasks = {task.name: task for task in task_list}
        self.done = set()

    def validate(self):
        for t in self.tasks.values():
            if any(d not in self.tasks for d in t.deps):
                raise WorkflowError("missing dependency")
            if t.name in t.deps:
                raise WorkflowError("self cycle")
        return True

    def run(self, handlers, retries=1):
        if isinstance(retries, bool) or not isinstance(retries, int) or retries < 0:
            raise ValueError("retries must be a non-negative integer")
        self.validate()
        pending = set(self.tasks) - self.done
        while pending:
            ready = [n for n in pending if set(self.tasks[n].deps) <= self.done]
            if not ready:
                raise WorkflowError("dependency cycle")
            for n in sorted(ready):
                err = None
                for _ in range(retries + 1):
                    try:
                        handlers[n]()
                        err = None
                        break
                    except Exception as e:
                        err = e
                if err:
                    raise WorkflowError(f"task failed: {n}") from err
                self.done.add(n)
                pending.remove(n)
        return sorted(self.done)
