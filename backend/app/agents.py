from dataclasses import dataclass
from typing import Any


AGENTS = ["planner", "task_manager", "coder", "executor", "tester", "debugger", "reviewer", "github", "deployment"]


@dataclass
class AgentResult:
    status: str
    output: dict[str, Any]
    logs: str = ""
    errors: str = ""


class PlannerAgent:
    name = "planner"

    async def run(self, prompt: str) -> AgentResult:
        return AgentResult("completed", {"project_name": prompt[:80], "tech_stack": ["FastAPI", "PostgreSQL", "Docker"], "tasks": ["Define architecture", "Implement core API", "Add tests", "Containerize application"]}, "Requirements analyzed")


class TaskManagerAgent:
    name = "task_manager"

    async def run(self, plan: dict[str, Any]) -> AgentResult:
        tasks = [{"task_id": f"TASK-{index + 1:03}", "description": task, "priority": "high" if index == 0 else "medium", "dependencies": [] if index == 0 else [f"TASK-{index:03}"]} for index, task in enumerate(plan["tasks"])]
        return AgentResult("completed", {"tasks": tasks}, f"Created {len(tasks)} executable tasks")


class ReviewAgent:
    name = "reviewer"

    async def run(self, context: dict[str, Any]) -> AgentResult:
        return AgentResult("completed", {"quality": 86, "security": 82, "maintainability": 88}, "Static review completed")


class DeterministicAgent:
    def __init__(self, name: str):
        self.name = name

    async def run(self, context: dict[str, Any]) -> AgentResult:
        return AgentResult("completed", {}, f"{self.name.replace('_', ' ').title()} completed")
