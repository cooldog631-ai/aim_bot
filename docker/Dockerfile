# Multi-stage build for smaller image
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY migrations/ ./migrations/
COPY alembic.ini ./
COPY .env.example ./

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create logs directory
RUN mkdir -p logs data

# Expose port for API
EXPOSE 8000

# Run bot by default
CMD ["python", "src/main.py"]
