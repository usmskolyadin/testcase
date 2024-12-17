from datetime import date, datetime
from sqlalchemy import Column, Table, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    telegram_id: Mapped[str] = mapped_column(String)

    tasks: Mapped["Task"] = relationship("Task", back_populates="user") # type: ignore
