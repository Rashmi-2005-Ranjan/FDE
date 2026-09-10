import httpx
import pytest

from app.main import create_app


@pytest.mark.asyncio
async def test_summarize_returns_generated_plain_text() -> None:
    async def fake_summarizer(ticket: str) -> str:
        assert ticket == "The checkout page returns a 500 error."
        return "Checkout is failing with a server error.\nThe issue blocks purchases."

    transport = httpx.ASGITransport(app=create_app(fake_summarizer))
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/summarize",
            content="The checkout page returns a 500 error.",
            headers={"Content-Type": "text/plain"},
        )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == (
        "Checkout is failing with a server error.\nThe issue blocks purchases."
    )


@pytest.mark.asyncio
async def test_summarize_rejects_empty_ticket() -> None:
    async def unused_summarizer(ticket: str) -> str:
        raise AssertionError("summarizer should not be called")

    transport = httpx.ASGITransport(app=create_app(unused_summarizer))
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/summarize",
            content="   ",
            headers={"Content-Type": "text/plain"},
        )

    assert response.status_code == 400
    assert response.text == "Ticket text is required."
