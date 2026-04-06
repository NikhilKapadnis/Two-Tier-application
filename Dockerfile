# ============================================================
#  Dockerfile — Flask + PostgreSQL app
#  Uses gunicorn as the production WSGI server (not flask dev)
# ============================================================

FROM python:3.11-alpine

# Install system deps needed by psycopg2
RUN apk add --no-cache gcc musl-dev libpq-dev

WORKDIR /app

# Copy and install dependencies first (Docker layer caching)
# If requirements.txt hasn't changed, this layer is reused on rebuild
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Port Flask/gunicorn listens on
EXPOSE 5000

# Use gunicorn in production — more stable than flask dev server
# workers=2 is fine for a small ECS task (0.5 vCPU / 1GB RAM)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
