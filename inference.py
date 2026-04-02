import os
from openai import OpenAI
from tasks import TASKS
from graders import grade

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def ask_model(subject, body, sender):
    prompt = f"""You are an email triage assistant.
Classify this email into exactly one of: reply, delete, escalate

Email:
Subject: {subject}
From: {sender}
Body: {body}

Reply with only one word: reply, delete, or escalate"""

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

def run_inference():
    print("Starting inference...")
    print("=" * 40)

    total_score = 0.0

    for task in TASKS:
        email = task["email"]
        action = ask_model(
            email["subject"],
            email["body"],
            email["sender"]
        )
        score = grade(task, action)
        total_score += score

        print(f"Task {task['task_id']} ({task['difficulty']})")
        print(f"  Correct: {task['correct_action']}")
        print(f"  Predicted: {action}")
        print(f"  Score: {score}")
        print()

    avg_score = total_score / len(TASKS)
    print("=" * 40)
    print(f"Average Score: {avg_score:.2f}")
    print("Inference complete!")

if __name__ == "__main__":
    run_inference()
