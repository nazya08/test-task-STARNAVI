from datetime import timedelta

from src.main.celery import celery_app


class CeleryService:
    def schedule_auto_reply(self, auto_reply: dict, delay: timedelta):
        celery_task = celery_app.send_task(
            "save_auto_reply",
            args=[auto_reply],
            countdown=delay.total_seconds()
        )
        return celery_task


celery_service = CeleryService()
