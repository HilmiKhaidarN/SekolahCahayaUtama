FROM python:3.9-slim

# Metadata
LABEL maintainer="Sekolah Cahaya Utama"
LABEL description="Platform belajar digital SDG 4 - Quality Education"

WORKDIR /app

# Install dependencies dulu (layer cache trick)
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ ./app/
COPY run.py .

# Buat direktori instance untuk SQLite database
RUN mkdir -p instance

# Non-root user untuk keamanan
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# Environment defaults — semua bisa di-override via Kubernetes ConfigMap
ENV SCHOOL_NAME="Sekolah Cahaya Utama"
ENV SCHOOL_TAGLINE="Belajar Cerdas, Berprestasi Gemilang"
ENV SECRET_KEY="change-me-in-production"
ENV DATABASE_URL="sqlite:////app/instance/sekolah.db"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Health check bawaan Docker
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Gunicorn: 2 workers, timeout 60s untuk /stress endpoint
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "--access-logfile", "-", "run:app"]
