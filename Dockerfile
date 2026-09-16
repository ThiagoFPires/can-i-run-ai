# Stage 1: Build do Frontend Vue 3
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Runtime do Backend Python FastAPI
FROM python:3.11-slim
WORKDIR /app

# Instalar dependências Python
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copiar código do backend
COPY backend/ ./backend/

# Copiar build do frontend para ser servido pelo FastAPI
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}"]
