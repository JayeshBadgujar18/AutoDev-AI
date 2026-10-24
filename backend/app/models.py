from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    prompt: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="planning")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    tasks: Mapped[list["Task"]] = relationship(cascade="all, delete-orphan")
    executions: Mapped[list["Execution"]] = relationship(cascade="all, delete-orphan")


class Agent(Base):
    __tablename__ = "agents"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    status: Mapped[str] = mapped_column(String(32), default="idle")
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    task_id: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    status: Mapped[str] = mapped_column(String(32), default="pending")
    dependencies: Mapped[list[str]] = mapped_column(JSON, default=list)


class Execution(Base):
    __tablename__ = "executions"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    agent: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(32))
    logs: Mapped[str] = mapped_column(Text, default="")
    errors: Mapped[str] = mapped_column(Text, default="")
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class MemoryEntry(Base):
    __tablename__ = "memory_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    kind: Mapped[str] = mapped_column(String(40))
    content: Mapped[str] = mapped_column(Text)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
