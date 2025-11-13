FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install

# Copy frontend files but exclude vite.config.ts
COPY frontend/src/ ./src/
COPY frontend/index.html ./
COPY frontend/*.json ./
COPY frontend/*.js ./
COPY frontend/*.ts ./

# Remove any problematic config file
RUN rm -f vite.config.ts

# Build with default Vite configuration
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY --from=frontend-builder /app/frontend/dist ./static

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]