from typing import Optional

from src.adapters.repositories.common.auto_reply import AutoReplyReader, AutoReplySaver
from src.adapters.sqlalchemy.db.session import SessionLocal
from src.adapters.sqlalchemy.models import AutoReplySettings


class AutoReplyDbGateway(AutoReplyReader, AutoReplySaver):
    def __init__(self, session: SessionLocal):
        self.session = session

    def get_settings_by_user_id(self, user_id: int) -> Optional[AutoReplySettings]:
        return self.session.query(AutoReplySettings).filter_by(user_id=user_id).first()

    def save_settings(self, settings: AutoReplySettings):
        self.session.add(settings)
        self.session.commit()

    def update_settings(self, settings: AutoReplySettings):
        self.session.commit()
