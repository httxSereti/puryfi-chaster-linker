from cuid2 import cuid_wrapper
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

cuid = cuid_wrapper()


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=cuid,
        nullable=False,
    )
