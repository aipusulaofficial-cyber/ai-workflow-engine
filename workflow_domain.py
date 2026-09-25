from dataclasses import dataclass,field
from enum import StrEnum

class State(StrEnum): PENDING="pending"; RUNNING="running"; SUCCEEDED="succeeded"; FAILED="failed"

@dataclass
class Workflow:
    steps:list[str]; state:State=State.PENDING; completed:list[str]=field(default_factory=list)
    def start(self):
        if self.state is not State.PENDING: raise ValueError("workflow already started")
        self.state=State.RUNNING
    def complete_step(self,step:str):
        if self.state is not State.RUNNING or step not in self.steps: raise ValueError("invalid step")
        if step not in self.completed:self.completed.append(step)
        if len(self.completed)==len(self.steps):self.state=State.SUCCEEDED

def retry_allowed(attempt:int,max_attempts:int)->bool:return 0<=attempt<max_attempts
