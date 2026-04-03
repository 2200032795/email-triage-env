---
title: Email Triage Env
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
tags:
  - openenv
---

## Email Triage Environment

An OpenEnv environment where an AI agent learns to triage emails
by deciding to reply, delete, or escalate them.
This simulates a real-world task that humans do every day.

## Motivation

Email overload is a real problem. This environment trains AI agents
to automatically sort emails saving time and improving productivity.

## Action Space

- reply - Send a reply to the email
- delete - Delete the email (spam or irrelevant)
- escalate - Forward to manager (urgent issues)

## Observation Space

- email_id: Unique email ID
- subject: Email subject line
- body: Email body text
- sender: Sender email address
- step: Current step number
- max_steps: Maximum steps allowed

## Tasks

- Task 1 (Easy): Delete obvious spam email - Score 1.0
- Task 2 (Medium): Reply to meeting request - Score 1.0
- Task 3 (Hard): Escalate urgent server issue - Score 1.0

## Reward Function

- 1.0 = Correct action
- 0.3 to 0.4 = Partially correct
- 0.0 = Wrong action

## Setup

pip install -r requirements.txt

python -m uvicorn server:app --reload --port 7860

python inference.py

## Baseline Scores

- Task 1 Easy: 1.0
- Task 2 Medium: 1.0
- Task 3 Hard: 1.0
- Average: 1.0

## Environment URL

https://huggingface.co/spaces/LaxmiVarshini/email-triage-env