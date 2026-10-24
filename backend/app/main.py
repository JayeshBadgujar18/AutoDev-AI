from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .config import get_settings
from .db import get_db, init_db
from .memory import search_memory, store_memory
from .models import Agent, Execution, Project, Task
from .schemas import ExecutionRead, MemoryCreate, ProjectCreate, ProjectRead, WorkflowEvent
from .workflow import workflow

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", description="Autonomous software engineering control plane")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
async def startup() -> None:
    await init_db()
    async with get_db().__anext__() as _:
        pass


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/agents")
async def agents(db: AsyncSession = Depends(get_db)) -> list[dict]:
    rows = list((await db.scalars(select(Agent))).all())
    return [{"name": row.name, "status": row.status, "last_run_at": row.last_run_at} for row in rows]


@app.get("/api/projects", response_model=list[ProjectRead])
async def list_projects(db: AsyncSession = Depends(get_db)) -> list[Project]:
    return list((await db.scalars(select(Project).order_by(Project.created_at.desc()))).all())


@app.post("/api/projects", response_model=ProjectRead, status_code=201)
async def create_project(payload: ProjectCreate, db: AsyncSession = Depends(get_db)) -> Project:
    project = Project(name=payload.name or payload.prompt[:60], prompt=payload.prompt)
    db.add(project)
    await db.flush()
    result = await workflow.ainvoke({"prompt": payload.prompt, "events": []})
    project.status = "completed"
    for item in result.get("tasks", []):
        db.add(Task(project_id=project.id, **item))
    for event in result.get("events", []):
        db.add(Execution(project_id=project.id, agent=event["node"], status=event["status"], logs=event["message"]))
    await db.commit()
    await db.refresh(project)
    return project


@app.get("/api/projects/{project_id}/executions", response_model=list[ExecutionRead])
async def project_executions(project_id: int, db: AsyncSession = Depends(get_db)) -> list[Execution]:
    return list((await db.scalars(select(Execution).where(Execution.project_id == project_id).order_by(Execution.created_at))).all())


@app.post("/api/memory", status_code=201)
async def create_memory(payload: MemoryCreate, db: AsyncSession = Depends(get_db)) -> dict:
    memory = await store_memory(db, payload)
    return {"id": memory.id, "kind": memory.kind, "content": memory.content}


@app.get("/api/memory")
async def memories(query: str = Query(min_length=1), project_id: int | None = None, db: AsyncSession = Depends(get_db)) -> list[dict]:
    return [{"id": item.id, "kind": item.kind, "content": item.content, "metadata": item.metadata} for item in await search_memory(db, query, project_id)]


@app.get("/api/workflow/demo", response_model=list[WorkflowEvent])
async def workflow_demo() -> list[dict[str, str]]:
    result = await workflow.ainvoke({"prompt": "Build a FastAPI Todo Application", "events": []})
    return result["events"]
