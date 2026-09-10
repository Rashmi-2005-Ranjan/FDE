from types import SimpleNamespace
from typing import Any

import pytest

from app.service import summarize_ticket


class FakeResponses:
    def __init__(self) -> None:
        self.request: dict[str, Any] | None = None

    async def create(self, **request: Any) -> SimpleNamespace:
        self.request = request
        return SimpleNamespace(output_text="Line one.\nLine two.")


@pytest.mark.asyncio
async def test_summarize_sends_expected_prompt_and_model() -> None:
    responses = FakeResponses()
    client = SimpleNamespace(responses=responses)

    result = await summarize_ticket(
        "Printer is offline.", client=client, model="test-model"  # type: ignore[arg-type]
    )

    assert result == "Line one.\nLine two."
    assert responses.request == {
        "model": "test-model",
        "input": "Summarize this support ticket in 2 lines : \n\nPrinter is offline.",
        "store": False,
    }
