# ALL-TIME XI Production Dockerfile
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PORT=8000

# Install system dependencies & Korean fonts for Pillow PNG rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-nanum \
    fonts-noto-cjk \
    fonts-dejavu-core \
    libfreetype6-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and pre-seeded database
COPY . .

# Ensure data & cache directories exist
RUN mkdir -p data/image_cache public

# Expose default port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/countries || exit 1

# Start Uvicorn with PORT environment variable support
CMD ["sh", "-c", "python -X utf8 -m uvicorn server.app:app --host 0.0.0.0 --port ${PORT}"]
