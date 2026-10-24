from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import MemoryEntry
from .schemas import MemoryCreate


async def store_memory(db: AsyncSession, entry: MemoryCreate) -> MemoryEntry:
    memory = MemoryEntry(**entry.model_dump())
    db.add(memory)
    await db.commit()
    await db.refresh(memory)
    return memory


async def search_memory(db: AsyncSession, query: str, project_id: int | None = None) -> list[MemoryEntry]:
    statement = select(MemoryEntry).where(MemoryEntry.content.ilike(f"%{query}%"))
    if project_id is not None:
        statement = statement.where(MemoryEntry.project_id == project_id)
    return list((await db.scalars(statement.order_by(MemoryEntry.created_at.desc()))).all())
