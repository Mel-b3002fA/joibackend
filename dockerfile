# Use a Python base image with GPU support
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Copy Poetry files and install dependencies
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-root --no-interaction --no-ansi

# Copy application files
COPY . .

# Expose port for Hugging Face Spaces
EXPOSE 7860

# Start FastAPI server
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]