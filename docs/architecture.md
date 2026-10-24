# AutoDev AI architecture

AutoDev AI is split into a Next.js control plane and an async FastAPI orchestration API. The API owns durable project state and exposes a LangGraph workflow that composes isolated agents.

## Workflow

`Planner -> Task Manager -> Code Generator -> Execution -> Testing -> Review -> GitHub -> Deployment`

A failed testing node routes to the Debugger and loops back to Code Generator. The current workflow keeps execution deterministic for local development; model-backed implementations can replace each agent's `run` method without changing the graph or API contract.

## Persistence

SQLAlchemy models cover projects, agents, tasks, executions, and memory entries. PostgreSQL is the production database. SQLite is the default local database so the API can boot without external infrastructure. Qdrant is the target long-term vector store; the memory service currently provides a durable relational fallback and a stable interface for adding embeddings.
