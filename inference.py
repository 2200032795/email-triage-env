import os
import asyncio
from typing import List, Optional
from openai import OpenAI
from tasks import TASKS
from graders import grade

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
BENCHMARK = "email-triage-env"
SUCCESS_SCORE_THRESHOLD = 0.5

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def ask_model(client: OpenAI, subject: str, body: str, sender: str) -> str:
    prompt = f"""You are an email triage assistant.
Classify this email into exactly one of: reply, delete, escalate

Email:
Subject: {subject}
From: {sender}
Body: {body}

Reply with only one word: reply, delete, or escalate"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.0
        )
        action = response.choices[0].message.content.strip().lower()
        if action not in ["reply", "delete", "escalate"]:
            action = "reply"
        return action
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "reply"

def run_inference():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    for task in TASKS:
        task_name = f"task_{task['task_id']}_{task['difficulty']}"
        rewards = []
        steps_taken = 0
        success = False

        log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

        try:
            email = task["email"]
            action = ask_model(client, email["subject"], email["body"], email["sender"])
            reward = grade(task, action)
            done = True
            steps_taken = 1
            rewards.append(reward)

            log_step(step=1, action=action, reward=reward, done=done, error=None)

            score = reward
            success = score >= SUCCESS_SCORE_THRESHOLD

        finally:
            log_end(success=success, steps=steps_taken, score=sum(rewards), rewards=rewards)

if __name__ == "__main__":
    run_inference()