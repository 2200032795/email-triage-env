def grade(task: dict, action: str) -> float:
    correct = task["correct_action"]

    # Exact match — full score
    if action == correct:
        return 1.0

    # Partial scores — wrong but not terrible
    if correct == "escalate" and action == "reply":
        return 0.3  # replied instead of escalating — partial credit

    if correct == "reply" and action == "escalate":
        return 0.4  # escalated instead of replying — partial credit

    if correct == "delete" and action == "reply":
        return 0.1  # replied to spam — very wrong

    if correct == "delete" and action == "escalate":
        return 0.0  # escalated spam — completely wrong

    if correct == "reply" and action == "delete":
        return 0.0  # deleted important email — completely wrong

    if correct == "escalate" and action == "delete":
        return 0.0  # deleted urgent issue — completely wrong

    return 0.0


def grade_all(tasks: list, actions: list) -> dict:
    results = {}
    for task, action in zip(tasks, actions):
        score = grade(task, action)
        results[task["task_id"]] = {
            "difficulty": task["difficulty"],
            "correct_action": task["correct_action"],
            "agent_action": action,
            "score": score
        }
    return results