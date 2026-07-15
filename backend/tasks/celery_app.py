from celery import Celery

celery = Celery(
    "trekking_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "tasks.reminder_tasks",
        "tasks.report_tasks",
        "tasks.export_tasks"
    ]
)

celery.conf.timezone = "Asia/Kolkata"

celery.conf.beat_schedule = {
    "daily-reminder": {
        "task": "tasks.reminder_tasks.daily_reminder",
        "schedule": 60.0
    },
    "monthly-report": {
        "task": "tasks.report_tasks.monthly_report",
        "schedule": 120.0
    }
}