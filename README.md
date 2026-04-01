# Email Triage Environment

An OpenEnv environment where an AI agent learns to triage emails
by deciding to reply, delete, or escalate them.

## Tasks

| Task | Difficulty | Description |
|------|-----------|-------------|
| Task 1 | Easy | Delete obvious spam email |
| Task 2 | Medium | Reply to meeting request |
| Task 3 | Hard | Escalate urgent server issue |

## Action Space
- reply
- delete
- escalate

## Observation Space
- email_id
- subject
- body
- sender
- step
- max_steps

## Reward
- 1.0 = correct action
- 0.0 to 0.4 = partial credit
- 0.0 = wrong action

## Setup

Install dependencies:
```
pip install -r requirements.txt
```

Run server:
```
python -m uvicorn server:app --reload --port 7860
```

Run inference:
```
python inference.py
```

## Baseline Scores
- Task 1 (Easy): 1.0
- Task 2 (Medium): 1.0
- Task 3 (Hard): 1.0
- Average: 1.0