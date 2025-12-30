FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY flask_app/ flask_app/
COPY migrations/ migrations/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .
ENV FLASK_ENV=prod
ENV PORT=5000
EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
