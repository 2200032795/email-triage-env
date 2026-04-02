## Email Triage Environment

An OpenEnv environment where an AI agent learns to triage emails
by deciding to reply, delete, or escalate them.
This simulates a real-world task that humans do every day.

## Motivation

Email overload is a real problem. This environment trains AI agents
to automatically sort emails saving time and improving productivity.

## Action Space

The agent can take one of 3 actions:
- reply — Send a reply to the email
- delete — Delete the email (spam or irrelevant)
- escalate — Forward to manager (urgent issues)

## Observation Space

| Field | Type | Description |
|-------|------|-------------|
| email_id | int | Unique email ID |
| subject | str | Email subject line |
| body | str | Email body text |
| sender | str | Sender email address |
| step | int | Current step number |
| max_steps | int | Maximum steps allowed |

## Tasks

| Task | Difficulty | Description | Expected Score |
|------|-----------|-------------|----------------|
| Task 1 | Easy | Delete obvious spam email | 1.0 |
| Task 2 | Medium | Reply to meeting request | 1.0 |
| Task 3 | Hard | Escalate urgent server issue | 1.0 |

## Reward Function

- 1.0 — Correct action taken
- 0.3 to 0.4 — Partially correct action
- 0.0 — Wrong action taken

## Setup Instructions

Install dependencies:
```
pip install -r requirements.txt
```

Run server locally:
```
python -m uvicorn server:app --reload --port 7860
```

Run inference:
```
python inference.py
```

Docker build and run:
```
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

## Baseline Scores

| Task | Difficulty | Score |
|------|-----------|-------|
| Task 1 | Easy | 1.0 |
| Task 2 | Medium | 1.0 |
| Task 3 | Hard | 1.0 |
| Average | - | 1.0 |

## Environment URL

