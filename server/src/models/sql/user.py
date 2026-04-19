from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from models.sql.base import Base


class User(Base):
    __tablename__ = "users"

    # chaster user id
    chaster_user_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)

    # chaster username
    chaster_username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)

    # token used to link puryfi plugin with Chaster extension
    link_token: Mapped[str | None] = mapped_column(String(512), nullable=True)
    
    # if user has linked puryfi and chaster
    is_linked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
