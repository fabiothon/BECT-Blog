# BUILD STAGE
FROM python:3.14.4-slim-bookworm AS builder

# Copy UV binary from official image
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

WORKDIR /app

# UV Docker optimizations
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

# Create venv inside /app so it survives the copy into the production stage
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies first (cached if unchanged)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# COPY pyproject.toml uv.lock ./
# RUN uv sync --locked --no-install-project --no-dev

# Copy app code and install project
COPY . ./
# RUN uv sync --locked --no-dev

FROM python:3.14.4-slim-bookworm AS css

WORKDIR /app

ENV TAILWINDCSS_VERSION=v4.3.3

COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY static ./static
COPY templates ./templates
RUN tailwindcss -i static/css/input.css -o static/css/output.css --minify

# PRODUCTION STAGE
FROM python:3.14.4-slim-bookworm

WORKDIR /app

# Run as non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Copy app and dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /app /app
COPY --from=css --chown=appuser:appuser /app/static/css/output.css /app/static/css/output.css

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# exec replaces shell so fastapi receives SIGTERM for clean shutdown
CMD ["/bin/sh", "-c", "exec fastapi run --host 0.0.0.0 --port \"$PORT\" --proxy-headers --forwarded-allow-ips '*'"]