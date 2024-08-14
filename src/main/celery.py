from celery import Celery

from src.adapters.sqlalchemy.db.session import SessionLocal
from src.adapters.sqlalchemy.models import Comment
from src.main.config import settings

celery_app = Celery(
    "test_starnavi",
    broker=settings.BROKER_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery_app.autodiscover_tasks(["src.services.celery"])


@celery_app.task(name="save_auto_reply")
def save_auto_reply(auto_reply_data):
    db = SessionLocal()
    try:
        auto_reply = Comment(**auto_reply_data)
        db.add(auto_reply)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
