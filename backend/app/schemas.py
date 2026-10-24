from datetime import datetime
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    prompt: str = Field(min_length=8, max_length=5000)
    name: str | None = None


class TaskRead(BaseModel):
    id: int
    task_id: str
    description: str
    priority: str
    status: str
    dependencies: list[str]
    model_config = {"from_attributes": True}


class ProjectRead(BaseModel):
    id: int
    name: str
    prompt: str
    status: str
    created_at: datetime | None = None
    tasks: list[TaskRead] = []
    model_config = {"from_attributes": True}


class ExecutionRead(BaseModel):
    id: int
    agent: str
    status: str
    logs: str
    errors: str
    duration_ms: int
    created_at: datetime | None = None
    model_config = {"from_attributes": True}


class MemoryCreate(BaseModel):
    kind: str = Field(min_length=2, max_length=40)
    content: str = Field(min_length=2)
    project_id: int | None = None
    metadata: dict = {}


class WorkflowEvent(BaseModel):
    node: str
    status: str
    message: str
