from models import EmailObservation, EmailAction, EmailReward
from tasks import TASKS
from graders import grade

class EmailTriageEnv:
    def __init__(self):
        self.current_task_index = 0
        self.current_step = 0
        self.max_steps = 3
        self.done = False
        self.current_observation = None

    def reset(self):
        self.current_task_index = 0
        self.current_step = 0
        self.done = False
        task = TASKS[self.current_task_index]
        self.current_observation = EmailObservation(
            email_id=task["email"]["email_id"],
            subject=task["email"]["subject"],
            body=task["email"]["body"],
            sender=task["email"]["sender"],
            step=self.current_step,
            max_steps=self.max_steps
        )
        return self.current_observation

    def step(self, action: EmailAction):
        if self.done:
            return self.current_observation, EmailReward(
                reward=0.0,
                done=True,
                info="Episode already done"
            )

        task = TASKS[self.current_task_index]
        score = grade(task, action.action)

        reward = EmailReward(
            reward=score,
            done=False,
            info=f"Action: {action.action} | Correct: {task['correct_action']} | Score: {score}"
        )

        self.current_step += 1
        self.current_task_index += 1

        if self.current_task_index >= len(TASKS):
            self.done = True
            reward.done = True
            reward.info += " | All tasks complete!"
        else:
            task = TASKS[self.current_task_index]
            self.current_observation = EmailObservation(
                email_id=task["email"]["email_id"],
                subject=task["email"]["subject"],
                body=task["email"]["body"],
                sender=task["email"]["sender"],
                step=self.current_step,
                max_steps=self.max_steps
            )

        return self.current_observation, reward

    def state(self):
        return {
            "current_task_index": self.current_task_index,
            "current_step": self.current_step,
            "done": self.done,
            "current_observation": self.current_observation.dict()
            if self.current_observation else None
        }