# Use Python 3.13 to match GitHub Actions CI pipeline
FROM python:3.13-slim

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
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 5000

# Since packages are installed system-wide, we can run flask directly
CMD ["flask", "run", "--host=0.0.0.0"]