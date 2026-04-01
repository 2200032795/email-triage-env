TASKS = [
    {
        "task_id": 1,
        "difficulty": "easy",
        "email": {
            "email_id": 1,
            "subject": "WIN FREE IPHONE!!!",
            "body": "Click here to claim your free iPhone now! Limited time offer!",
            "sender": "promo@spam123.com"
        },
        "correct_action": "delete",
        "description": "Delete this obvious spam email"
    },
    {
        "task_id": 2,
        "difficulty": "medium",
        "email": {
            "email_id": 2,
            "subject": "Meeting tomorrow at 10am",
            "body": "Hi, can we schedule a meeting tomorrow at 10am to discuss the project update?",
            "sender": "colleague@company.com"
        },
        "correct_action": "reply",
        "description": "Reply to this meeting request from colleague"
    },
    {
        "task_id": 3,
        "difficulty": "hard",
        "email": {
            "email_id": 3,
            "subject": "URGENT: Production server is down!",
            "body": "Our production server stopped responding 10 minutes ago. Customers cannot access the website. Need immediate attention!",
            "sender": "alerts@company.com"
        },
        "correct_action": "escalate",
        "description": "Escalate this urgent server issue to manager"
    }
]