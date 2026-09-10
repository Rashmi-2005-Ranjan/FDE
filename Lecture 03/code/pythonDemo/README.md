# Python ticket summarizer

This is the Python/FastAPI equivalent of the Spring Boot project. It exposes the
same `POST /api/summarize` endpoint, accepts a support ticket as raw text, and
returns a plain-text two-line summary.

## Run

Requires Python 3.11 or newer.

```bash
cd pythonDemo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set your real `OPENAI_API_KEY` in `.env`, then start the API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}"
```

Test it with:

```bash
curl -X POST http://localhost:8080/api/summarize \
  -H "Content-Type: text/plain" \
  --data "Customers cannot complete checkout because the payment page times out."
```

For development and tests, install `requirements-dev.txt` and run `pytest`. The
tests use a fake OpenAI client and do not make paid API calls.
