from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from models.sql.base import Base


class UserLockConfiguration(Base):
    __tablename__ = "users_lock_configurations"

    # Chaster lock identifier
    lock_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)

    # Chaster session identifier
    session_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)

    # Token used to link the Puryfi plugin with the Chaster extension
    link_token: Mapped[str | None] = mapped_column(String(512), nullable=True, unique=True, index=True)

    # Whether the Puryfi plugin is actively linked to this lock
    is_linked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Chaster user id of the keyholder
    keyholder_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)

    # Chaster user id of the wearer
    wearer_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)

    # configurations
    lock_password: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lock_on_freeze: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    unlock_on_unfreeze: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<UserLockConfiguration id={self.id!r} "
            f"lock_id={self.lock_id!r} is_linked={self.is_linked}>"
        )
