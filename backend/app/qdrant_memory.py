from qdrant_client import AsyncQdrantClient
from .config import get_settings


class QdrantMemory:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = AsyncQdrantClient(url=settings.qdrant_url)
        self.collection = settings.qdrant_collection

    async def search_memory(self, vector: list[float], limit: int = 8):
        return await self.client.search(collection_name=self.collection, query_vector=vector, limit=limit)
