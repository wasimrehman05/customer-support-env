FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY customer_support_env/server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy environment package
COPY customer_support_env/ /app/customer_support_env/

# Copy root files
COPY inference.py /app/
COPY README.md /app/

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start server
CMD ["uvicorn", "customer_support_env.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
