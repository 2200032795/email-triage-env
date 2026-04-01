from fastapi import FastAPI
from pydantic import BaseModel
from env import EmailTriageEnv
from models import EmailAction

app = FastAPI()
env = EmailTriageEnv()

class ActionRequest(BaseModel):
    action: str

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step(request: ActionRequest):
    action = EmailAction(action=request.action)
    obs, reward = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.reward,
        "done": reward.done,
        "info": reward.info
    }

@app.get("/state")
def state():
    return env.state()