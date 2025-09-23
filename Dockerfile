FROM python:3.13-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN uv sync --locked

CMD ["fastapi", "run", "--workers", "4", "main.py"]