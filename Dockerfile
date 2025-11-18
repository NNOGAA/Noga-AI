FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with extended timeout for large packages
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Copy the rest of the application
COPY . .

EXPOSE 8080

# Auto-initialize database then start server
CMD ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
