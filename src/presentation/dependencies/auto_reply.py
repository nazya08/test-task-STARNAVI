from fastapi import Depends
from sqlalchemy.orm import Session

from src.adapters.repositories.auto_reply import AutoReplyDbGateway
from src.presentation.dependencies.base import get_db
from src.services.auto_reply import AutoReplyService


def get_auto_reply_db_gateway(db: Session = Depends(get_db)) -> AutoReplyDbGateway:
    return AutoReplyDbGateway(session=db)


def get_auto_reply_service(auto_reply_db_gateway: AutoReplyDbGateway = Depends(get_auto_reply_db_gateway)) -> AutoReplyService:
    return AutoReplyService(auto_reply_db_gateway=auto_reply_db_gateway)
