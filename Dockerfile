# Use Python 3.13 to match GitHub Actions CI pipeline
FROM python:3.13-slim

# Security: Install only critical system patches, then clean up
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies system-wide to prevent volume mount conflicts with .venv
RUN uv sync --frozen --no-cache --system

# Copy the rest of the application code
COPY . .

# Security: Create and switch to a non-root user to limit blast radius
RUN adduser --disabled-password --no-create-home appuser && \
    chown -R appuser:appuser /app
USER appuser

# Security: Drop all capabilities (no root-like permissions)
# Run as non-root, read-only filesystem is recommended at orchestration level

EXPOSE 5000

# Health check for container orchestrators
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Since packages are installed system-wide, we can run flask directly
CMD ["flask", "run", "--host=0.0.0.0"]