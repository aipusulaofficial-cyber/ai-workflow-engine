"""Workflow engine with DAG validation, retries and idempotent task execution."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Task: name:str; deps:tuple[str,...]=()
class WorkflowError(Exception):pass
class Workflow:
 def __init__(self,tasks):self.tasks={t.name:t for t in tasks};self.done=set()
 def validate(self):
  for t in self.tasks.values():
   if any(d not in self.tasks for d in t.deps):raise WorkflowError("missing dependency")
   if t.name in t.deps:raise WorkflowError("self cycle")
  return True
 def run(self,handlers,retries=1):
  self.validate();pending=set(self.tasks)
  while pending:
   ready=[n for n in pending if set(self.tasks[n].deps)<=self.done]
   if not ready:raise WorkflowError("dependency cycle")
   for n in sorted(ready):
    if n in self.done:continue
    err=None
    for _ in range(retries+1):
     try:handlers[n]();err=None;break
     except Exception as e:err=e
    if err:raise WorkflowError(f"task failed: {n}") from err
    self.done.add(n);pending.remove(n)
  return list(self.done)
