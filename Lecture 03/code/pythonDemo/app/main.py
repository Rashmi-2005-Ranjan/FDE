import logging

from fastapi import FastAPI, Request, Response

from .service import Summarizer, summarize_ticket

logger = logging.getLogger(__name__)


def create_app(summarizer: Summarizer = summarize_ticket) -> FastAPI:
    app = FastAPI(title="Ticket Summarizer", docs_url=None, redoc_url=None)

    @app.post("/api/summarize", response_class=Response)
    async def summarize(request: Request) -> Response:
        try:
            ticket = (await request.body()).decode("utf-8")
        except UnicodeDecodeError:
            return Response(
                content="Ticket text must be valid UTF-8.",
                status_code=400,
                media_type="text/plain",
            )

        if not ticket.strip():
            return Response(
                content="Ticket text is required.",
                status_code=400,
                media_type="text/plain",
            )

        try:
            summary = await summarizer(ticket)
        except Exception:
            logger.exception("Failed to summarize ticket")
            return Response(
                content="Unable to summarize the ticket.",
                status_code=500,
                media_type="text/plain",
            )

        return Response(content=summary, media_type="text/plain")

    return app


app = create_app()
