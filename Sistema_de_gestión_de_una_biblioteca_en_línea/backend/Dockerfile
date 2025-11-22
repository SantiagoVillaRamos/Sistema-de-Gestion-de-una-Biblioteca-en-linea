# Lightweight Python base
FROM python:3.10-slim
# Set working directory
WORKDIR /app
# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy application source code
COPY . .
# Note: Actual execution is defined in docker-compose.yml
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009"]
