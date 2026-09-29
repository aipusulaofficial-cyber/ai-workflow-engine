import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workflow_domain import Workflow,State,retry_allowed
w=Workflow(["a","b"]); w.start(); w.complete_step("a"); mid=w.state.value; w.complete_step("b"); report={"mid_state":mid,"final_state":w.state.value,"retry_allowed":retry_allowed(1,3),"retry_exhausted":retry_allowed(3,3)}
if report!={"mid_state":"running","final_state":"succeeded","retry_allowed":True,"retry_exhausted":False}: raise SystemExit(report)
print(json.dumps(report,sort_keys=True))
