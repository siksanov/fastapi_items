from python:3.13-alpine

copy --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

copy . /app

ENV PATH="/app/.venv/bin:$PATH"

workdir /app

run uv sync --locked

CMD ["fastapi", "run", "--workers", "4", "api/main.py"]