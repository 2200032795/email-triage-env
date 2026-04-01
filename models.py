from pydantic import BaseModel
from typing import Optional

class EmailObservation(BaseModel):
    email_id: int
    subject: str
    body: str
    sender: str
    step: int
    max_steps: int

class EmailAction(BaseModel):
    action: str  # "reply", "delete", or "escalate"

class EmailReward(BaseModel):
    reward: float
    done: bool
    info: str