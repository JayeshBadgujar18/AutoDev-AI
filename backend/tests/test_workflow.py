import pytest
from app.workflow import workflow


@pytest.mark.asyncio
async def test_workflow_reaches_deployment():
    result = await workflow.ainvoke({"prompt": "Build a FastAPI Todo Application", "events": []})
    assert result["test_passed"] is True
    assert result["events"][-1]["node"] == "deployment"
    assert len(result["tasks"]) == 4
