# --- 1. Builder stage ---
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Set environment variables for the runtime
ENV PYTHONBUFFERED=1 \
    # Virtual environment path
    VENV_PATH="/opt/venv" \
    # Place entry points in the environment at the front of the path
    PATH="/opt/venv/bin:$PATH" \
    # Copy from the cache instead of linking since it's a mounted volume
    UV_LINK_MODE=copy

# Set environment variables for the runtime
RUN uv venv ${VENV_PATH}

# Set the working directory
WORKDIR /app

COPY pyproject.toml ./

# Activate venv and run uv pip sync
RUN bash -c ". '${VENV_PATH}/bin/activate'"

# Install project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable --no-dev

# Copy the project into the intermediate image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# ---  2. Final stage ---
FROM python:3.11-slim-bookworm AS final

LABEL maintainer="Carlos Espeleta" \
      description="A RAG system with FastAPI, LlamaIndex, ChromaDB, and HuggingFace models."

# Set environment variables for the runtime
ENV PYTHONBUFFERED=1 \
    VENV_PATH="/opt/venv" \
    PATH="/opt/venv/bin:$PATH" \
    HF_HOME="/app/hf_cache"

# Create a non-root user and group to run the application
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --create-home --home-dir /app appuser

WORKDIR /app

# Copy the environment, but not the source code
COPY --from=builder --chown=appuser:appgroup ${VENV_PATH} ${VENV_PATH}
COPY --from=builder --chown=appuser:appgroup /app/app/ ./app/
COPY --from=builder --chown=appuser:appgroup /app/config-local.yaml ./
COPY --from=builder --chown=appuser:appgroup /app/run.sh ./

# Create and set permissions for the Hugging Face cache directory
RUN mkdir -p "${HF_HOME}" \
    && chown -R appuser:appgroup "${HF_HOME}"

# Ensure the entrypoint script is executable by anyone
RUN chmod +x ./run.sh

# Switch to the non-root user
USER appuser

ENTRYPOINT [ "./run.sh" ]
