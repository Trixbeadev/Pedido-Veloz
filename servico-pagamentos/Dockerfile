FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5002

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --no-compile -r requirements.txt \
    && useradd --system --uid 10001 --create-home appuser
COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE 5002

CMD ["opentelemetry-instrument", "gunicorn", "--bind", "0.0.0.0:5002", "--workers", "2", "--threads", "4", "--worker-tmp-dir", "/dev/shm", "app:app"]