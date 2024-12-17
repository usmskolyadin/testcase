from datetime import date, datetime

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    message: Mapped[str] = mapped_column()
    user: Mapped["User"] = relationship("User", back_populates="tasks") # type: ignore
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))