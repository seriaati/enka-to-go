# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# git is required to resolve the enka git dependency in pyproject.toml
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (cached as long as the lockfile doesn't change)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.11-slim-bookworm

RUN groupadd -r app && useradd -r -g app -d /app app

# /app must stay writable by the app user: enka downloads its
# asset data into /app/.enka_py at runtime. The directory is created
# here so a named volume mounted at it inherits the app user's ownership.
COPY --from=builder --chown=app:app /app /app
RUN mkdir /app/.enka_py && chown app:app /app/.enka_py

ENV PATH="/app/.venv/bin:$PATH" \
    HOST=0.0.0.0

WORKDIR /app
USER app

EXPOSE 7091

CMD ["python", "run.py"]
