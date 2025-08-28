FROM python:latest

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create src directory for development mounting
RUN mkdir -p /app/src

# Copy source code (this will be overridden by volume in development)
COPY . /app/src

EXPOSE 8000

# Default command - can be overridden in docker-compose
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]