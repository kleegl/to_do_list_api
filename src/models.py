from datetime import UTC, datetime
from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Unicode, DateTime, Enum
from sqlalchemy.orm import Mapped, Relationship
from core import Base
import enum


class TaskStatus(enum.Enum):
    TO_DO = 0
    IN_WORK = 1
    COMPLETE = 2


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(256), unique=True, nullable=False)
    password_hash = Column(Unicode(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    tasks: Mapped[List["Task"]] = Relationship()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    content = Column(Unicode, nullable=True)
    created_at = Column(DateTime(timezone=True), insert_default=datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        insert_default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
    status = Column(Enum(TaskStatus), default=TaskStatus.TO_DO)
    user_id = Column(ForeignKey("users.id"))
