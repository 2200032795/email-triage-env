from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional, List
import uvicorn

try:
    from tasks import TASKS
except Exception as e:
    print(f"[ERROR] tasks import failed: {e}", flush=True)
    TASKS = []

try:
    from graders import grade
except Exception as e:
    print(f"[ERROR] graders import failed: {e}", flush=True)
    def grade(task, action):
        return 0.0

# ── In-memory state per task_id ───────────────────────────────────────────────
_state: dict = {}   # task_id -> {"done": bool, "action": str, "reward": float, "step": int}

def _get_task(task_id: int) -> dict:
    for t in TASKS:
        if t["task_id"] == task_id:
            return t
    return None

# ── Pydantic models ───────────────────────────────────────────────────────────
class ResetRequest(BaseModel):
    task_id: int

class StepRequest(BaseModel):
    task_id: int
    action: str   # "reply" | "escalate" | "delete"

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="email-triage-env")

@app.get("/")
@app.get("/health")
def health():
    return {"status": "ok", "env": "email-triage-env"}

@app.get("/tasks")
def list_tasks():
    """Return all task definitions so inference.py can iterate them."""
    return TASKS

@app.post("/reset")
def reset(req: ResetRequest):
    task = _get_task(req.task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"task_id {req.task_id} not found")
    _state[req.task_id] = {"done": False, "action": None, "reward": 0.0, "step": 0}
    return {
        "task_id": req.task_id,
        "observation": task["email"],
        "status": "reset",
    }

@app.post("/step")
def step(req: StepRequest):
    task = _get_task(req.task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"task_id {req.task_id} not found")

    valid_actions = {"reply", "escalate", "delete"}
    if req.action not in valid_actions:
        raise HTTPException(status_code=400, detail=f"action must be one of {valid_actions}")

    reward = grade(task, req.action)
    done   = True   # single-step environment

    _state[req.task_id] = {
        "done":   done,
        "action": req.action,
        "reward": reward,
        "step":   1,
    }

    return {
        "task_id":    req.task_id,
        "action":     req.action,
        "reward":     reward,
        "done":       done,
        "observation": task["email"],
        "info": {
            "correct_action": task["correct_action"],
            "description":    task["description"],
        },
    }

@app.get("/state")
def state(task_id: int):
    task = _get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"task_id {task_id} not found")
    s = _state.get(task_id, {"done": False, "action": None, "reward": 0.0, "step": 0})
    return {
        "task_id":     task_id,
        "observation": task["email"],
        **s,
    }

@app.get("/results")
def results():
    out = []
    for task in TASKS:
        tid = task["task_id"]
        s   = _state.get(tid, {})
        out.append({
            "task_id":    tid,
            "difficulty": task["difficulty"],
            "done":       s.get("done", False),
            "action":     s.get("action"),
            "reward":     s.get("reward", 0.0),
        })
    return {"results": out}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)