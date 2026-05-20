FROM node:20-slim AS frontend-build

WORKDIR /build/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/
COPY --from=frontend-build /build/frontend/dist ./frontend/dist

WORKDIR /app/backend

ENV DEBUG=false
ENV ALLOWED_HOSTS=*
ENV GEOCODING_ENABLED=true

EXPOSE 8080

CMD gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8080} \
    --timeout 120 \
    --workers 1 \
    --access-logfile - \
    --error-logfile - \
    --capture-output
