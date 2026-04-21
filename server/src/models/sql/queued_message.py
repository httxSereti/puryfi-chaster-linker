from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from models.sql.base import Base

class QueuedMessage(Base):
    __tablename__ = "queued_messages"
    
    link_token: Mapped[str] = mapped_column(String(512), index=True)
    msg_type: Mapped[str] = mapped_column(String(128))
    payload: Mapped[dict] = mapped_column(JSON)
