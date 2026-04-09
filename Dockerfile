FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

# Используем Gunicorn вместо Flask development server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]
